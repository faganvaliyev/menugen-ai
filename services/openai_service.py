from openai import OpenAI
from config.settings import OPENAI_MODEL, INGREDIENTS_PROMPT_TEMPLATE
from typing import Optional

class OpenAIService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
    
    def get_ingredients(self, dish_name: str) -> str:
        """Get ingredients for a dish using OpenAI API"""
        if not dish_name or not dish_name.strip():
            return "Error: Dish name cannot be empty"
        
        prompt = INGREDIENTS_PROMPT_TEMPLATE.format(dish=dish_name.strip())
        
        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful culinary assistant who provides accurate ingredient lists for dishes."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300,  
                timeout=30  
            )
            
            content = response.choices[0].message.content
            if not content:
                return "Error: No response received from OpenAI"
            
            return content.strip()
            
        except Exception as e:
            
            if "rate_limit" in str(e).lower():
                return "Error: API rate limit exceeded. Please try again later."
            elif "authentication" in str(e).lower():
                return "Error: Invalid API key or authentication failed."
            elif "timeout" in str(e).lower():
                return "Error: Request timed out. Please try again."
            else:
                return f"Error: {str(e)}"
    
    def get_ingredients_with_quantities(self, dish_name: str) -> Optional[dict]:
        """Get main ingredients with approximate quantities"""
        if not dish_name or not dish_name.strip():
            return None
        
        detailed_prompt = f"""
        For the dish "{dish_name.strip()}", provide only the main ingredients with approximate quantities.
        
        Format as a simple list, for example:
        - 2 cups rice
        - 1 lb chicken breast
        - 1 onion, diced
        """
        
        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a culinary assistant who provides ingredient lists with quantities. Only list main ingredients with approximate amounts."},
                    {"role": "user", "content": detailed_prompt}
                ],
                temperature=0.5,
                max_tokens=300,
                timeout=30
            )
            
            content = response.choices[0].message.content
            if content:
                return {
                    "dish_name": dish_name.strip(),
                    "ingredients": content.strip(),
                    "success": True
                }
            
            return None
            
        except Exception as e:
            return {
                "dish_name": dish_name.strip(),
                "error": str(e),
                "success": False
            }
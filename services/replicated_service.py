import replicate
from typing import Optional, Tuple
import time

REPLICATE_MODEL = "ideogram-ai/ideogram-v3-turbo"

class ImageGenerationService:
    """Generates realistic images of dishes using Replicate API"""
   
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.client = replicate.Client(api_token=api_token)
   
    def generate_image(self, dish_name: str) -> Tuple[Optional[str], Optional[str]]:
        if not dish_name or not dish_name.strip():
            return None, "Dish name cannot be empty"
       
        try:
            prompt = f"A realistic photo of {dish_name}, food photography, cinematic lighting, 4K, studio background"
            
            print(f"Generating image for: {dish_name}")
            print(f"Using model: {REPLICATE_MODEL}")
            print(f"Prompt: {prompt}")
            
           
            prediction = self.client.predictions.create(
                model=REPLICATE_MODEL,
                input={
                    "prompt": prompt,
                    "aspect_ratio": "1:1"
                }
            )
            
            print(f"Prediction created with ID: {prediction.id}")
            print(f"Initial status: {prediction.status}")
            
            
            max_wait_time = 120  
            start_time = time.time()
            
            while prediction.status not in ["succeeded", "failed", "canceled"]:
                if time.time() - start_time > max_wait_time:
                    return None, "Image generation timed out"
                
                time.sleep(2)
                prediction.reload()
                print(f"Status: {prediction.status}")
            
            if prediction.status == "succeeded":
                output = prediction.output
                print(f"Generation successful! Output type: {type(output)}")
                print(f"Output content: {output}")
                
              
                if isinstance(output, list) and len(output) > 0:
                    first = output[0]
                    if isinstance(first, str) and first.startswith("http"):
                        return first, None
                    elif hasattr(first, 'url'): 
                        return first.url, None
                
                if isinstance(output, str) and output.startswith("http"):
                    return output, None
                
                if hasattr(output, 'url'):
                    return output.url, None
                
                return None, f"Unexpected output format: {type(output)} - {output}"
                
            elif prediction.status == "failed":
                error_msg = getattr(prediction, 'error', 'Unknown error')
                return None, f"Image generation failed: {error_msg}"
            else:
                return None, f"Image generation was canceled or failed with status: {prediction.status}"
                
        except replicate.exceptions.ReplicateError as e:
            print(f"Replicate API error: {str(e)}")
            if "401" in str(e) or "Unauthenticated" in str(e):
                return None, "Invalid API token"
            elif "404" in str(e):
                return None, f"Model not found: {REPLICATE_MODEL}"
            else:
                return None, f"Replicate API error: {str(e)}"
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None, f"Unexpected error: {str(e)}"
    
    def test_connection(self) -> Tuple[bool, str]:
        """Test if the API connection is working"""
        try:
            
            models = list(self.client.models.list())
            return True, "Connection successful"
        except replicate.exceptions.ReplicateError as e:
            if "401" in str(e) or "Unauthenticated" in str(e):
                return False, "Invalid API token"
            else:
                return False, f"API error: {str(e)}"
        except Exception as e:
            return False, f"Connection error: {str(e)}"
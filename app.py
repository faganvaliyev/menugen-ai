import streamlit as st
from PIL import Image
import os
from dotenv import load_dotenv
from services.ocr_service import OCRService
from services.openai_service import OpenAIService
from services.replicated_service import ImageGenerationService
from config.settings import APP_TITLE, APP_DESCRIPTION

st.set_page_config(page_title=APP_TITLE, layout="centered")
st.title(APP_TITLE)
st.markdown(APP_DESCRIPTION)

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
replicate_api_key = os.getenv("REPLICATE_API_KEY") or os.getenv("REPLICATE_API_TOKEN")

if not openai_api_key:
    st.error("❌ OpenAI API key is missing. Please add OPENAI_API_KEY to your .env file.")
    st.stop()
if not replicate_api_key:
    st.error("❌ Replicate API key is missing. Please add REPLICATE_API_KEY to your .env file.")
    st.stop()

uploaded_file = st.file_uploader("📷 Upload or take a picture of the menu", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Menu", use_container_width=True)

    with st.spinner("🔍 Extracting dish names..."):
        ocr_service = OCRService()
        raw_text = ocr_service.extract_text(image)
        dish_names = ocr_service.extract_dish_names(raw_text)
    if dish_names:
        st.success("✅ Dishes detected! Select the ones you'd like to analyze.")
        selected_dishes = st.multiselect("🍽️ Select dishes:", dish_names)
        if selected_dishes:
            openai_service = OpenAIService(openai_api_key)
            image_service = ImageGenerationService(replicate_api_key)
            for dish in selected_dishes:
                st.markdown(f"---\n### 🍛 {dish}")
                
                with st.spinner("🧠 Getting ingredients..."):
                    ingredients = openai_service.get_ingredients(dish)
                st.markdown(f"Ingredients:\n{ingredients}")
                connection_ok, message = image_service.test_connection()
                if not connection_ok:
                    st.error(f"❌ Connection test failed: {message}")
                else:
                    st.success(f"✅ {message}")
                
                with st.spinner("🎨 Generating image..."):
                    image_url, error = image_service.generate_image(dish)
                    if image_url:
                        if isinstance(image_url, list) and len(image_url) > 0:
                            image_url = image_url[0]
                        try:
                            st.image(image_url, caption=f"AI-generated image of {dish}", use_container_width=True)
                        except Exception as e:
                            st.error(f"❌ Failed to display image: {str(e)}")
                            st.info("The image was generated but couldn't be displayed.")
                            st.markdown(f"[View generated image]({image_url})")
                    else:
                        st.error(f"❌ Image generation failed: {error}")
        else:
            st.info("👆 Please select at least one dish to analyze.")
    else:
        st.error("❌ No dish names could be extracted. Try another image.")
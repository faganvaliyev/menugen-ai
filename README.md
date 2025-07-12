# MenuGen AI 🍽️🤖

MenuGen AI is an intelligent Streamlit-based application that:
- 📷 Extracts **dish names** from restaurant **menu images**
- 🧠 Uses **ChatGPT** (OpenAI API) to retrieve **ingredients** for selected dishes
- 🎨 Generates **realistic dish images** using **Replicate's Flux-Pro model**

---

## 🚀 Features

- Multilingual OCR (supports Azerbaijani + English)
- Enhanced confidence filtering and manual editing
- OpenAI GPT-based ingredient generation
- Realistic food photo generation via Replicate AI
- Clean and interactive Streamlit UI

---

## 🔧 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/menugen-ai.git
   cd menugen-ai

## 📁 Project Structure

menugen-ai/
├── app.py
├── config/
│   └── settings.py
├── services/
│   ├── ocr_service.py
│   ├── openai_service.py
│   └── replicated_service.py
├── .env.example
├── requirements.txt
└── README.md

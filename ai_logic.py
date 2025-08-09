import os
from datetime import datetime
from deep_translator import GoogleTranslator
from langdetect import detect
from openai import OpenAI


client = OpenAI(
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# 1. Language Detection
def detect_language(text):
    try:
        return detect(text)
    except:
        return 'en'

# 2. Translation functions
def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except:
        return text

SUPPORTED_LANGUAGES = [
    'hi', 'gu', 'bn', 'ta', 'te', 'kn', 'ml', 'mr', 'ur', 'pa',
    'fr', 'de', 'es', 'it', 'pt', 'ru', 'ja', 'zh', 'ko'
]

def translate_back(text, target_lang):
    try:
        if target_lang not in SUPPORTED_LANGUAGES or target_lang == 'en':
            return text
        return GoogleTranslator(source='en', target=target_lang).translate(text)
    except:
        return text

# 3. Emotional reply using GPT (via OpenRouter)
def generate_emotional_reply(input_text):
    lang = detect_language(input_text)
    english_text = translate_to_english(input_text)

    prompt = f"""You are a caring, warm, and empathetic friend.
Respond to the following message with emotional support, compassion, and gentle encouragement. Suggest some small activity or exersice in very bad mood or emotion to improve mood and stay calm.
Do not ask questions, just provide comfort, love, and hope. Give short ,sweet and consice 4-5 line response. don't give a big paragraph and don't be too short.
User: {english_text}
Friend:"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": "You are a compassionate emotional support assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=150
        )
        ai_reply = response.choices[0].message.content.strip()
    except Exception as e:
        print("[ERROR] AI request failed:", e)
        ai_reply = "I'm here for you. You're not alone."

    return translate_back(ai_reply, lang)

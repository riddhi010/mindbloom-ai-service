from transformers import pipeline
from deep_translator import GoogleTranslator
from datetime import datetime

# Lightweight model loaded once
sentiment_pipeline = pipeline("sentiment-analysis")

# Emotional Reply Logic
def generate_emotional_reply(text, emotion):
    text = text.lower()
    if 'alone' in text or 'lonely' in text:
        return "It’s okay to feel alone sometimes. Just know you matter and your voice is heard. ❤️"
    elif 'tired' in text or 'exhausted' in text:
        return "You deserve rest. Please take a moment to breathe and care for yourself. 🌸"
    elif 'happy' in text or 'joy' in text:
        return "That’s wonderful to hear! Keep holding on to that joy 😊"
    elif emotion == 'negative':
        return "I'm here for you. Whatever you're feeling is valid. Sending love 💖"
    elif emotion == 'positive':
        return "That's beautiful. I'm so glad you're feeling this way! 🌼"
    else:
        return "Thank you for opening up. You're not alone. Take a gentle step forward today 💫"



# Translation Functions
def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except:
        return text

def translate_back(text, target_lang):
    try:
        if target_lang == 'en':
            return text
        return GoogleTranslator(source='en', target=target_lang).translate(text)
    except:
        return text

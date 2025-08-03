from transformers import pipeline
from deep_translator import GoogleTranslator
import sqlite3
from datetime import datetime

# Load sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# --- Emotion Detection ---
def detect_emotion(text):
    result = sentiment_pipeline(text)[0]
    label = result['label'].lower()
    if label == 'negative':
        return 'negative'
    elif label == 'positive':
        return 'positive'
    else:
        return 'neutral'

# --- DB Helper Functions ---
def init_db():
    conn = sqlite3.connect('mindbloom_user_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    goal TEXT,
                    day INTEGER,
                    feedback TEXT,
                    emotion TEXT,
                    next_activity TEXT,
                    timestamp TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# --- Goal-based activity pool ---
goal_activities = {
    "stress relief": [
        "Take a 5-minute breathing break.",
        "Write down 3 things you're grateful for.",
        "Listen to calming music for 10 minutes.",
        "Take a short walk outside.",
        "Practice a 2-minute body scan meditation."
    ],
    "focus improvement": [
        "Work in a distraction-free environment for 20 mins.",
        "Write your top 3 tasks for the day.",
        "Try the Pomodoro technique for a task.",
        "Read a book for 15 minutes without interruptions.",
        "Do a quick brain dump journaling exercise."
    ],
    "self-confidence": [
        "Write down one thing you’re proud of today.",
        "Stand tall and do a power pose for 2 minutes.",
        "Recall a time when you succeeded at something.",
        "Compliment yourself in the mirror.",
        "List 3 of your unique strengths."
    ]
}

# --- Main Logic ---
def generate_response(text, user_id=None, goal=None):
    emotion = detect_emotion(text)
    day = 1
    next_activity = "Keep going, you're doing great!"

    # Fetch last activity for user
    if user_id and goal:
        conn = sqlite3.connect('mindbloom_user_data.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM user_progress WHERE user_id=? AND goal=?", (user_id, goal))
        day = c.fetchone()[0] + 1

        # Cycle activities from pool based on day
        pool = goal_activities.get(goal.lower(), [])
        if pool:
            next_activity = pool[(day - 1) % len(pool)]

        # Save progress
        c.execute('''INSERT INTO user_progress (user_id, goal, day, feedback, emotion, next_activity, timestamp)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (user_id, goal, day, text, emotion, next_activity, datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()

    # Emotionally supportive reply
    if 'alone' in text.lower() or 'lonely' in text.lower():
        support = "It’s okay to feel alone sometimes. Just know you matter and your voice is heard. ❤️"
    elif 'tired' in text.lower() or 'exhausted' in text.lower():
        support = "You deserve rest. Please take a moment to breathe and care for yourself. 🌸"
    elif 'happy' in text.lower() or 'joy' in text.lower():
        support = "That’s wonderful to hear! Keep holding on to that joy 😊"
    elif emotion == 'negative':
        support = "I'm here for you. Whatever you're feeling is valid. Sending love 💖"
    elif emotion == 'positive':
        support = "That's beautiful. I'm so glad you're feeling this way! 🌼"
    else:
        support = "Thank you for opening up. You're not alone. Take a gentle step forward today 💫"

    return f"{support}\n\n🌱 Your next activity for {goal.title() if goal else 'your goal'} (Day {day}):\n➡️ {next_activity}"

# --- Translation ---
def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except:
        return text

def translate_back(text, target_lang):
    try:
        return GoogleTranslator(source='en', target=target_lang).translate(text)
    except:
        return text

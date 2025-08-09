# MindBloom AI Service

Empowering users with empathy through multilingual, emotionally supportive AI responses.

## Features

### 🤝 Empathic AI Response
Generates warm, compassionate replies to anonymous user posts — aimed at offering comfort, encouragement, and human-like emotional support.

### 🌐 Multi-Language Support
Automatically translates user input to English, feeds it into an AI model, and translates responses back into the user's language for seamless global accessibility.

### ⚙️ Simple Microservice Architecture
Built with Flask for easy integration into existing apps, with minimal dependencies and clear separation of logic (AI engine, translation, language detection).

---

## Repository Structure
```bash
mindbloom-ai-service/
├── ai_logic.py             # Core logic: translation, language detection, GPT-powered reply generation
├── app.py                  # Flask API (route: /analyze) exposing the microservice
├── requirements.txt        # Python package dependencies
└── .gitignore

```

## Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/riddhi010/mindbloom-ai-service.git
cd mindbloom-ai-service
```
2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
3️⃣ Configure Environment Variables
Create a .env file in the project root and add:
```bash
OPENAI_API_KEY=your_openai_or_openrouter_key_here
```
4️⃣ Run the Service
```bash
python app.py
```
- Now you can add your working URL to the mindbloom backend to handle Multi language support AI response for Anonymous post.
- You can deploy it using Hugging Face Spaces

# 🧑‍💻 Author
Riddhi Shah 

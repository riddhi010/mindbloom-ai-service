import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from ai_logic import (
    generate_emotional_reply,
    translate_to_english,
    translate_back,
    sentiment_pipeline  # Reuse the already-loaded pipeline
)

app = Flask(__name__)
CORS(app)

# Route: Anonymous journal chat - emotional support only
@app.route('/analyze', methods=['POST'])
def analyze_chat():
    data = request.json
    user_text = data.get('text', '')
    lang = data.get('lang', 'en')

    # Step 1: Translate to English for processing
    translated_text = translate_to_english(user_text)

    # Step 2: Sentiment detection
    try:
        emotion_result = sentiment_pipeline(translated_text)[0]
        emotion_label = emotion_result['label'].lower()  # 'POSITIVE' or 'NEGATIVE'
    except:
        emotion_label = 'neutral'

    # Step 3: Generate emotional response
    ai_reply = generate_emotional_reply(translated_text, emotion_label)

    # Step 4: Translate back if necessary
    if lang != 'en':
        ai_reply = translate_back(ai_reply, lang)

    return jsonify({ "reply": ai_reply })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # For Render/Fly.io compatibility
    app.run(host='0.0.0.0', port=port)

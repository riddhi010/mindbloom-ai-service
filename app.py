import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # <- import this
from ai_logic import (
    generate_emotional_reply,
    translate_to_english,
    translate_back
)

app = Flask(__name__)
CORS(app)
# Route 1: Anonymous journal chat - emotional support only
@app.route('/analyze', methods=['POST'])
def analyze_chat():
    data = request.json
    user_text = data.get('text', '')
    lang = data.get('lang', 'en')

    translated_text = translate_to_english(user_text)
    ai_reply = generate_emotional_reply(translated_text)  # No user_id or goal for chat

    if lang != 'en':
        ai_reply = translate_back(ai_reply, lang)

    return jsonify({ "reply": ai_reply })



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Render sets PORT env variable
    app.run(host='0.0.0.0', port=port)

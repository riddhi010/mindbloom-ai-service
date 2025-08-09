import os
from flask import Flask, request, jsonify
from flask_cors import CORS



from ai_logic import (
    generate_emotional_reply,
    translate_to_english,
    translate_back,
    detect_language
)

app = Flask(__name__)
CORS(app)

# Route: Anonymous journal chat - emotional support only
@app.route('/analyze', methods=['POST'])
def analyze_chat():
    data = request.json
    user_text = data.get('text', '')

    # Step 0: Auto-detect language
    lang = detect_language(user_text)
    print(f"[DEBUG] Detected language: {lang}", flush=True)

    # Step 1: Translate to English
    translated_text = translate_to_english(user_text)
    print(f"[DEBUG] Translated input: {translated_text}", flush=True)

    # Step 2: Generate AI emotional reply using BlenderBot
    ai_reply_en = generate_emotional_reply(translated_text)
    print(f"[DEBUG] AI English reply: {ai_reply_en}", flush=True)

    # Step 3: Translate reply back to original language (if needed)
    ai_reply = translate_back(ai_reply_en, lang) if lang != 'en' else ai_reply_en
    print(f"[DEBUG] Final translated reply: {ai_reply}", flush=True)

    return jsonify({ "reply": ai_reply })




if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7860))  # For Render/Fly.io compatibility
    app.run(host='0.0.0.0', port=port, debug=True)

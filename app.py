from flask import Flask, request, jsonify
from flask_cors import CORS  # <- import this
from ai_logic import (
    generate_response,
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
    ai_reply = generate_response(translated_text)  # No user_id or goal for chat

    if lang != 'en':
        ai_reply = translate_back(ai_reply, lang)

    return jsonify({ "reply": ai_reply })

# Route 2: Exercise page - goal-based daily activity generation
@app.route('/generate-activity', methods=['POST'])
def generate_activity():
    data = request.json
    user_text = data.get('text', '')
    user_id = data.get('user_id', 'default_user')
    goal = data.get('goal', None)
    lang = data.get('lang', 'en')

    translated_text = translate_to_english(user_text)
    activity_response = generate_response(translated_text, user_id=user_id, goal=goal)

    if lang != 'en':
        activity_response = translate_back(activity_response, lang)

    return jsonify({ "activity": activity_response })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render sets PORT env variable
    app.run(host='0.0.0.0', port=port)

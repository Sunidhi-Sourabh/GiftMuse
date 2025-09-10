from flask import Flask, request, jsonify
from config import GEMINI_API_KEY
import requests

app = Flask(__name__)

@app.route('/generate-bundle', methods=['POST'])
def generate_bundle():
    data = request.json
    prompt = build_prompt(data)
    
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
        headers=headers,
        json=payload
    )

    result = response.json()
    return jsonify(result)

def build_prompt(data):
    return f"""
    Suggest a personalized gift bundle for the following occasion:
    - Occasion: {data['occasion']}
    - Recipient: {data['relation']} ({data['recipient_gender']})
    - Budget: ₹{data['budget']}
    - Preferred product rating: {data['rating']}+ stars
    - Likes: {data['likes']}
    - Dislikes: {data['dislikes']}
    Use only products from this catalog. Return bundle items with reasoning, trust score, and delivery ETA.
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

from flask import Flask, request, jsonify
from config import GEMINI_API_KEY
import requests

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "<h2>GiftMuse is running. Use POST /generate-bundle to test Gemini.</h2>"

print("🔐 API Key Loaded:", GEMINI_API_KEY)

@app.route('/generate-bundle', methods=['POST'])
def generate_bundle():
    data = request.get_json()
    print("✅ Received data:", data)

    prompt = build_prompt(data)
    print("🧠 Constructed prompt:", prompt)

    print("🔐 Loaded API Key:", GEMINI_API_KEY if GEMINI_API_KEY else "❌ Not loaded")

    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            headers=headers,
            json=payload
        )
        print("📡 Gemini raw response:", response.text)
        result = response.json()
        return jsonify(result)
    except Exception as e:
        print("❌ Gemini call failed:", str(e))
        return jsonify({"error": "Gemini call failed", "details": str(e)})

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

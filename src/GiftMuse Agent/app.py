from flask import Flask, request, jsonify, render_template
import requests
import os
from config import GEMINI_API_KEY

app = Flask(__name__)

# 🔹 Homepage route (for HTML form or Vue mount point)
@app.route("/")
def home():
    return render_template("index.html")  # fallback form or Vue mount

# 🔹 HTML form submission route
@app.route("/result", methods=["POST"])
def result():
    try:
        data = request.form.to_dict()
        print("📥 Form data received:", data)

        prompt = build_prompt(data)
        print("🧠 Prompt constructed:", prompt)

        headers = {
    "Content-Type": "application/json",
    "x-goog-api-key": GEMINI_API_KEY
}

        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        response = requests.post(
            "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent",
            headers=headers,
            json=payload
        )

        bundle = response.json()
        print("🎁 Gemini response:", bundle)

        return render_template("result.html", bundle=bundle)

    except Exception as e:
        print("❌ Error in /result route:", str(e))
        return render_template("result.html", bundle={"error": str(e)})

# 🔹 Vue/JS API route
@app.route("/generate-bundle", methods=["POST"])
def generate_bundle():
    data = request.get_json()
    print("📦 Received JSON:", data)

    prompt = build_prompt(data)
    print("🧠 Prompt from API:", prompt)

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
        result = response.json()
        print("🎁 Gemini response:", result)
        return jsonify(result)
    except Exception as e:
        print("❌ Gemini API error:", str(e))
        return jsonify({"error": "Gemini call failed", "details": str(e)})

# 🔹 Prompt builder
def build_prompt(data):
    return f"""
    Suggest a personalized gift bundle for the following occasion:
    - Occasion: {data.get('occasion')}
    - Recipient: {data.get('relation')} ({data.get('recipient_gender')})
    - Budget: ₹{data.get('budget')}
    - Preferred product rating: {data.get('rating')}+ stars
    - Likes: {data.get('likes')}
    - Dislikes: {data.get('dislikes')}
    Use only products from this catalog. Return bundle items with reasoning, trust score, and delivery ETA.
    """

# 🔹 Run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

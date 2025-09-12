from flask import Flask, request, jsonify, render_template
import requests
import os
from config import GEMINI_API_KEY

app = Flask(__name__)

# 🔹 Homepage route (dashboard layout)
@app.route("/")
def home():
    return render_template("index.html", prompt=None, bundle=None)

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

        return render_template("index.html", prompt=prompt, bundle=bundle)

    except Exception as e:
        print("❌ Error in /result route:", str(e))
        return render_template("index.html", bundle={"error": str(e)})

# 🔹 Vue/JS API route (same Gemini endpoint)
@app.route("/generate-bundle", methods=["POST"])
def generate_bundle():
    try:
        data = request.get_json()
        print("📦 Received JSON:", data)

        prompt = build_prompt(data)
        print("🧠 Prompt from API:", prompt)

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

        result = response.json()
        print("🎁 Gemini response:", result)
        return jsonify(result)

    except Exception as e:
        print("❌ Gemini API error:", str(e))
        return jsonify({"error": "Gemini call failed", "details": str(e)})

# 🔹 Prompt builder
def build_prompt(data):
    prompt = f"Suggest a personalized gift bundle for {data.get('relation')} ({data.get('recipient_gender')}) on {data.get('occasion')} within ₹{data.get('budget')}."
    if data.get("likes"):
        prompt += f" They like {data.get('likes')}."
    if data.get("dislikes"):
        prompt += f" Avoid {data.get('dislikes')}."
    if data.get("rating"):
        prompt += f" Prefer products rated {data.get('rating')}+ stars."
    prompt += " Use only products from this catalog. Return bundle items with reasoning, trust score, and delivery ETA."
    return prompt

# 🔹 Run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

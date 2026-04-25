from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("API_KEY")

@app.route("/")
def home():
    return "API Running 🚀"

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        text = data.get("context")

        if not text:
            return jsonify({"error": "No input"}), 400

        # 🔥 STRONG PROMPT
        prompt = f"""
Generate 3 different and meaningful questions from the given paragraph.

Rules:
- Do NOT ask generic questions
- Questions must be based on facts
- Keep them clear and short

Paragraph:
{text}

Questions:
"""

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )

        result = response.json()

        output = result["choices"][0]["message"]["content"]

        # 🔥 CLEAN PARSING
        questions = []
        for line in output.split("\n"):
            line = line.strip()
            if line:
                questions.append(line)

        return jsonify({"questions": questions})

    except Exception as e:
        return jsonify({"error": str(e)})
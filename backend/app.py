from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

HF_API_KEY = os.environ.get("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

def query_hf(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        return response.json()
    except:
        return None


@app.route("/")
def home():
    return "AI Question Generator LIVE 🚀"


@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json(force=True)
        text = data.get("context", "")

        if not text:
            return jsonify({"error": "No input provided"}), 400

        prompt = f"""
Generate 3 simple questions from this text:

{text}
"""

        result = query_hf({"inputs": prompt})

        # 🔥 SAFE HANDLING (IMPORTANT FIX)
        if not result or isinstance(result, str):
            return jsonify({"error": "AI service failed"}), 500

        output = ""

        if isinstance(result, list) and "generated_text" in result[0]:
            output = result[0]["generated_text"]
        else:
            output = str(result)

        # convert to questions
        questions = [
            q.strip() + "?"
            for q in output.split("?")
            if len(q.strip()) > 5
        ]

        if not questions:
            questions = [
                "What is the main idea of the text?",
                "Explain the concept in the paragraph.",
                "What do you understand from the passage?"
            ]

        return jsonify({
            "questions": questions[:5]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
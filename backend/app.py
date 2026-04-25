from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# 🔐 HuggingFace API Key (Render ENV se)
HF_API_KEY = os.environ.get("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

# -----------------------------
# 🔥 SAFE API CALL FUNCTION
# -----------------------------
def query_hf(payload):
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        # ❗ if API fails
        if response.status_code != 200:
            print("HF STATUS ERROR:", response.text)
            return None

        try:
            return response.json()
        except:
            return None

    except Exception as e:
        print("HF REQUEST ERROR:", e)
        return None


# -----------------------------
# 🏠 HOME ROUTE
# -----------------------------
@app.route("/")
def home():
    return "AI Question Generator LIVE 🚀"


# -----------------------------
# 🧠 GENERATE QUESTIONS
# -----------------------------
@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json(force=True)
        text = data.get("context", "")

        if not text:
            return jsonify({"error": "No input provided"}), 400

        prompt = f"""
Generate 3 simple questions from this paragraph:

{text}
"""

        result = query_hf({"inputs": prompt})

        # -----------------------------
        # 🔥 FALLBACK SYSTEM (IMPORTANT)
        # -----------------------------
        if not result:
            return jsonify({
                "questions": [
                    "What is the main idea of the paragraph?",
                    "Explain the concept mentioned in the text.",
                    "What do you understand from the given passage?"
                ]
            })

        output = ""

        if isinstance(result, list) and "generated_text" in result[0]:
            output = result[0]["generated_text"]
        else:
            output = str(result)

        # -----------------------------
        # ✂️ CLEAN OUTPUT
        # -----------------------------
        questions = [
            q.strip() + "?"
            for q in output.split("?")
            if len(q.strip()) > 5
        ]

        # fallback again if empty
        if not questions:
            questions = [
                "What is the main idea?",
                "Explain the topic.",
                "What did you learn from this paragraph?"
            ]

        return jsonify({
            "questions": questions[:5]
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# -----------------------------
# 🚀 RUN SERVER
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
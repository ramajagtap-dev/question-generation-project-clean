from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# 🔐 API KEY from Render ENV
HF_API_KEY = os.environ.get("HF_API_KEY")

# 🚀 MISTRAL MODEL (IMPORTANT CHANGE)
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

# -----------------------------
# 🔥 API CALL FUNCTION
# -----------------------------
def query_hf(payload):
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            print("HF ERROR:", response.text)
            return None

        try:
            return response.json()
        except:
            return None

    except Exception as e:
        print("REQUEST ERROR:", e)
        return None


# -----------------------------
# 🏠 HOME ROUTE
# -----------------------------
@app.route("/")
def home():
    return "Mistral AI Question Generator LIVE 🚀"


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

        # 🔥 STRONG MISTRAL PROMPT (IMPORTANT)
        prompt = f"""
[INST]
You are an expert teacher.

Read the paragraph carefully and generate 5 different exam questions ONLY from the content.

Paragraph:
{text}

Rules:
- Questions must be context-based
- No generic questions
- No repetition
- Mix factual + conceptual + application questions

Return only numbered questions.
[/INST]
"""

        result = query_hf({"inputs": prompt})

        # -----------------------------
        # 🔥 FALLBACK SYSTEM
        # -----------------------------
        if not result:
            return jsonify({
                "questions": [
                    "What is the main idea of the paragraph?",
                    "What information is given in the text?",
                    "How can this concept be used in real life?",
                    "Explain the key concept mentioned.",
                    "Why is this topic important?"
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
        questions = []

        for line in output.split("\n"):
            line = line.strip()

            # remove numbering noise
            line = line.replace("1.", "").replace("2.", "").replace("3.", "")
            line = line.replace("4.", "").replace("5.", "").replace("-", "")

            if "?" in line and len(line) > 10:
                questions.append(line.strip())

        # fallback safety
        if len(questions) < 3:
            questions = [
                "What is explained in the paragraph?",
                "What are the key points mentioned?",
                "How is this useful in real life?",
                "Explain the main concept.",
                "What did you understand from the text?"
            ]

        return jsonify({
            "questions": questions[:5]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# 🚀 RUN SERVER
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
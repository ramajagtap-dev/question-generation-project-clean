from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import os

app = Flask(__name__)
CORS(app)

# ✅ FIX: use text-generation (NOT text2text-generation)
qg = pipeline(
    "text-generation",
    model="google/flan-t5-small"
)

@app.route("/")
def home():
    return "AI Question Generator Running 🚀"

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    text = data.get("context", "")

    if not text:
        return jsonify({"error": "No input provided"}), 400

    # 🧠 Prompt (SQuAD-inspired logic)
    prompt = f"""
Generate 3 different WH questions from the following paragraph:

{text}

Questions:
"""

    try:
        result = qg(
            prompt,
            max_new_tokens=120,
            do_sample=True,
            temperature=0.9,
            top_p=0.95
        )

        output = result[0]["generated_text"]

        # ✂️ Convert output into list
        questions = [
            q.strip() + "?"
            for q in output.split("?")
            if len(q.strip()) > 10
        ]

        if not questions:
            questions = ["What is the main idea of the text?"]

        return jsonify({
            "questions": questions[:5]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
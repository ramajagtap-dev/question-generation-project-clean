from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app)

# 🔥 AI MODEL
qg = pipeline("text2text-generation", model="google/flan-t5-small")

@app.route("/")
def home():
    return "AI Question Generator Running 🚀"

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    text = data.get("context", "")

    if not text:
        return jsonify({"error": "No input"}), 400

    # 🔥 SQuAD STYLE PROMPT
    prompt = f"""
Generate 3 different WH questions from this text:

{text}
"""

    result = qg(prompt, max_length=128, do_sample=True, temperature=0.9)

    output = result[0]["generated_text"]

    # split into questions
    questions = [q.strip() for q in output.split("?") if len(q.strip()) > 10]
    questions = [q + "?" for q in questions]

    if not questions:
        questions = ["What is the main idea of the text?"]

    return jsonify({"questions": questions[:5]})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app)

# 🔥 Load model once
generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-small"
)

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

        # 🔥 STRONG PROMPT (KEY CHANGE)
        prompt = f"""
Read the paragraph and generate 3 different and specific questions.

Rules:
- Do NOT ask "main idea"
- Questions must be different
- Questions must be based on facts in paragraph

Paragraph:
{text}

Output format:
1.
2.
3.
"""

        result = generator(
            prompt,
            max_length=200,
            do_sample=True,      # 🔥 randomness
            temperature=0.9,     # 🔥 variation
            top_k=50,
            top_p=0.95
        )

        output = result[0]["generated_text"]

        # 🔥 STRONG PARSING
        lines = output.split("\n")
        questions = []

        for line in lines:
            line = line.strip()
            if line and "?" in line:
                questions.append(line)

        # fallback (important)
        if len(questions) < 2:
            questions = [output.strip()]

        return jsonify({"questions": questions})

    except Exception as e:
        return jsonify({"error": str(e)})
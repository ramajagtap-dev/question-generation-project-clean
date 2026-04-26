from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import os

app = Flask(__name__)
CORS(app)

# =========================
# MODEL
# =========================
print("Loading model...")

qg_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"   # better than small
)

print("Model loaded ✅")


# =========================
# CORE FUNCTION
# =========================
def generate_questions(context):

    prompt = f"""
Generate 5 high-quality questions from the paragraph below.

Rules:
- Questions must be based only on given paragraph
- Do not repeat same type of questions
- Focus on who, what, where, why, how

Paragraph:
{context}

Output format:
1.
2.
3.
4.
5.
"""

    result = qg_pipeline(
        prompt,
        max_length=256,
        do_sample=True,
        temperature=0.8
    )

    text = result[0]["generated_text"]

    # clean output
    questions = []

    for line in text.split("\n"):
        line = line.strip()
        if len(line) > 5:
            questions.append(line)

    return questions[:5]


# =========================
# API
# =========================
@app.route("/")
def home():
    return jsonify({"message": "AI Question Generator Running 🚀"})


@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()

        if not data or "context" not in data:
            return jsonify({"error": "No context provided"}), 400

        context = data["context"]

        questions = generate_questions(context)

        return jsonify({
            "questions": questions
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
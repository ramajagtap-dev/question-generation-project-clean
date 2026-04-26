from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
from data_loader import get_dataset
import os

app = Flask(__name__)
CORS(app)

# =========================
# MODEL LOAD
# =========================
print("Loading AI model...")

qg_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-small"
)

print("Model loaded successfully ✅")


# =========================
# QUESTION GENERATION
# =========================
def generate_questions(context):

    prompt = f"""
Generate 5 simple and clear questions from the paragraph below:

Paragraph:
{context}

Questions:
"""

    result = qg_pipeline(
        prompt,
        max_length=128,
        do_sample=False
    )

    text = result[0]["generated_text"]

    # clean split into list
    questions = [
        q.strip()
        for q in text.split("?")
        if q.strip()
    ]

    # add ? back for proper format
    questions = [q + "?" if not q.endswith("?") else q for q in questions]

    return questions[:5]


# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return jsonify({"message": "AI Question Generator is running 🚀"})


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
        return jsonify({
            "error": str(e)
        }), 500


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
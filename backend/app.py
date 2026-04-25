from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app)

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

        questions_set = set()

        # 🔥 Run model 3 times for diversity
        for i in range(3):
            prompt = f"Generate one specific question from this text:\n{text}"

            result = generator(
                prompt,
                max_length=80,
                do_sample=True,
                temperature=0.9
            )

            q = result[0]["generated_text"].strip()

            if "?" not in q:
                q += "?"

            questions_set.add(q)

        # convert to list
        questions = list(questions_set)

        return jsonify({"questions": questions})

    except Exception as e:
        return jsonify({"error": str(e)})
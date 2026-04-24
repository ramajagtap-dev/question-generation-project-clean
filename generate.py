from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

generator = pipeline("text2text-generation", model="google/flan-t5-small")

@app.route("/")
def home():
    return "Server is running ✅"

@app.route("/generate", methods=["POST"])
def generate_question():
    try:
        data = request.get_json()
        context = data.get("context")

        if not context:
            return jsonify({"error": "No context provided"}), 400

        result = generator(
            f"generate a question from this paragraph: {context}",
            max_length=64
        )

        question = result[0]['generated_text']

        return jsonify({"question": question})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
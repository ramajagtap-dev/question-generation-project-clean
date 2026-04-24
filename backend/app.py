from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os
import torch

app = Flask(__name__)
CORS(app)

# Load model (make sure qg_model folder is inside backend/)
tokenizer = AutoTokenizer.from_pretrained("qg_model")
model = AutoModelForSeq2SeqLM.from_pretrained("qg_model")

@app.route("/")
def home():
    return "🚀 AI Question Generator API Running"

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        text = data.get("context")

        if not text:
            return jsonify({"error": "No input text provided"}), 400

        input_text = f"generate question: {text}"

        inputs = tokenizer(input_text, return_tensors="pt", truncation=True)

        outputs = model.generate(
            **inputs,
            max_new_tokens=50
        )

        question = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return jsonify({
            "input": text,
            "question": question
        })

    except Exception as e:
        return jsonify({"error": str(e)})

# IMPORTANT: Render compatibility
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
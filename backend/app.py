from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from data_loader import get_squad_examples
import random

app = Flask(__name__)

print("Loading model...")

model_name = "google/flan-t5-small"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

print("Model loaded ✅")

# SQuAD data
squad_data = get_squad_examples(100)


@app.route("/")
def home():
    return "🚀 Question Generation API is running!"


@app.route("/generate", methods=["POST"])
def generate_questions():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    prompt = f"""
    Read the paragraph and generate 3 specific questions based on it.

    Paragraph: {text}

    Questions:
    """

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)

    outputs = model.generate(
        **inputs,
        max_length=128,
        num_beams=5,
        early_stopping=True,
        no_repeat_ngram_size=2
    )

    questions = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return jsonify({
        "input_text": text,
        "questions": questions
    })


@app.route("/squad-sample", methods=["GET"])
def squad_sample():
    return jsonify(random.choice(squad_data))


if __name__ == "__main__":
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
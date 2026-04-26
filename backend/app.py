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

    prompt = f"Generate 3 questions from this paragraph: {text}"

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)

    outputs = model.generate(
        **inputs,
        max_length=128,
        do_sample=True,
        temperature=0.7
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
    app.run(debug=True)
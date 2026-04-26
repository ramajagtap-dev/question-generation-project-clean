from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)

model_name = "google/flan-t5-small"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

@app.route("/")
def home():
    return "AI Question Generator Running ✅"

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        context = data.get("context", "")

        if not context:
            return jsonify({"error": "No context provided"}), 400

        prompt = f"""
        Generate 5 different questions from this paragraph:

        {context}
        """

        inputs = tokenizer(prompt, return_tensors="pt", truncation=True)

        outputs = model.generate(
            **inputs,
            max_new_tokens=120,
            do_sample=True,
            temperature=0.7
        )

        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return jsonify({
            "questions": answer
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
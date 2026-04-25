from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# 🔑 API KEY LOAD
API_KEY = os.getenv("API_KEY")

# 🔍 DEBUG CHECK (temporary)
print("API KEY LOADED:", API_KEY)

@app.route("/")
def home():
    return "API Running 🚀"

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        text = data.get("context", "")

        if not text:
            return jsonify({"error": "No input"}), 400

        prompt = f"""
Generate 3 different and meaningful questions from this paragraph:

{text}
"""

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 120
            },
            timeout=15
        )

        result = response.json()

        # 🔍 DEBUG OUTPUT
        print("OPENAI RESPONSE:", result)

        if "choices" not in result:
            return jsonify({"error": result}), 500

        output = result["choices"][0]["message"]["content"]

        questions = [q.strip("- ").strip() for q in output.split("\n") if q.strip()]

        return jsonify({"questions": questions})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
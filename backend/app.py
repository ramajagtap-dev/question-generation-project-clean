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
        "max_tokens": 100
    },
    timeout=15
)

result = response.json()

# 🔥 DEBUG PRINT (IMPORTANT)
print("API RESPONSE:", result)

# 🔥 SAFE CHECK
if "choices" not in result:
    return jsonify({"error": result})

output = result["choices"][0]["message"]["content"]
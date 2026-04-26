import requests

url = "http://127.0.0.1:5000/generate"

data = {
    "text": "Artificial Intelligence is used in healthcare and education."
}

response = requests.post(url, json=data)

print(response.json())
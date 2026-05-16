from flask import Flask, request, jsonify
import requests
from openai import OpenAI

app = Flask(__name__)

NEWS_API = "2e3f64b4d09e465f8ae2ec32b2ff53ab"

client = OpenAI(api_key="YOUR_OPENAI_KEY")

@app.route("/news")
def news():

    url = f"https://newsapi.org/v2/top-headlines?language=en&apiKey={NEWS_API}"

    data = requests.get(url).json()

    headlines = []

    for article in data["articles"][:5]:
        headlines.append(article["title"])

    return jsonify(headlines)

@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json["message"]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    return jsonify({
        "reply": response.choices[0].message.content
    })

if __name__ == "__main__":
    app.run(debug=True)

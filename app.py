from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Set up OpenAI API credentials
openai.api_key = os.getenv("OPENAI_API_KEY")
messages = [{"role": "system", "content": "You are a Aggriculture expert with multilingual support. Assist farmers with your aggriculture and farming knowledge."}]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api", methods=["POST"])
def api():
    user_input = request.json.get("message")

    if not user_input:
        return jsonify({"error": "Message not provided"}), 400

    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    chatbot_response = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": chatbot_response})

    return jsonify({"response": chatbot_response}), 200


if __name__ == '__main__':
    app.run()

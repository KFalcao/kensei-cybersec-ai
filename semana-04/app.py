import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request

from gemini_client import GeminiClient

load_dotenv()

app = Flask(__name__)

gemini = GeminiClient.from_env()


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(force=True)
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "Missing required field: prompt"}), 400

    try:
        result = gemini.generate_text(prompt)
        return jsonify({"prompt": prompt, "response": result})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

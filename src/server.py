import json

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from src.client import get_relevant_summary, generate_reply

DEBUG = True
app = Flask(
    __name__,
    static_url_path="",
    static_folder="../client/dist",
    template_folder="../client/dist",
)
app.config.from_object(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/query", methods=["POST"])
def get_triplets():
    if request.method != "POST":
        return []
    data = json.loads(request.data)
    dialogue_lines = data["dialogue"]
    query = data["query"]
    prologue = data["prologue"]
    summary = get_relevant_summary(query, prologue)
    dialogue = "\n".join(dialogue_lines[-5:])
    return jsonify({"reply": generate_reply(summary, dialogue, query)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

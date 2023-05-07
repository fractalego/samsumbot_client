import json

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from src.connector import Connector

_connector = Connector()

DEBUG = True
app = Flask(
    __name__,
    static_url_path="",
    static_folder="../client/dist",
    template_folder="../client/dist",
)
app.config.from_object(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.before_request
def before_request():
    if not request.is_secure:
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/query", methods=["POST"])
def get_triplets():
    if request.method != "POST":
        return []
    data = json.loads(request.data)
    user_lines = data["user_lines"]
    bot_lines = data["bot_lines"]
    prologue = data["prologue"]
    return jsonify(
        {"reply": _connector.generate_reply(prologue, bot_lines, user_lines)}
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

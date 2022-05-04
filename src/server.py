from flask import Flask, render_template
from flask_cors import CORS

DEBUG = True
app = Flask(__name__,
            static_url_path='',
            static_folder='../client/dist',
            template_folder='../client/dist')
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)

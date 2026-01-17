from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "FLASK HIDUP DI RAILWAY"

@app.route("/test")
def test():
    return "TEST OK"

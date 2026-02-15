from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def about():
    return render_template("about.html")
@app.route("/home")
def home():
    return render_template("home.html")
@app.route("/index1")
def index1():
    return render_template("index1.html")
@app.route("/index2")
def index2():
    return render_template("index2.html")


if __name__ == "__main__":
    app.run(debug=True,port=5001)

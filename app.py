from flask import Flask, render_template

app = Flask(__name__)
# 2 -- get your flask app into the repo
# 3 -- get the data to display in HTML as plain text


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
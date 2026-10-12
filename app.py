from flask import Flask, render_template
from bus_scraper import BusAPI
app = Flask(__name__)
# 3 -- get the data to display in HTML as plain text

api = BusAPI()
data = api.get_data()
print(data)

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
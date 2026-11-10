from flask import Flask, render_template
from bus_scraper import BusAPI
import test_times_data
app = Flask(__name__)
import bus_scraper
# 3 -- get the data to display in HTML as plain text

api = BusAPI()


@app.route("/")
def home():
    data = test_times_data.data #was a single list, now a touple of two lists. First is departure, second is arrival.
    return render_template("index.html", data=data)
    print(data)


if __name__ == "__main__":
    app.run(debug=True)
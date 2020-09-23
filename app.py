# Dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

# instance and connection
app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# route index.html
@app.route("/")
def home():

    # find record
    destination_data = mongo.db.collection.find_one()

    # return template/data
    return render_template("index.html", mars=destination_data)

# route trigger for scrape
@app.route("/scrape")
def scrape():

    # run scrape
    mars_data = scrape_mars.scrape_mars()

    # update Mongo DB
    mongo.db.collection.update({}, mars_data, upsert=True)

    # redirect
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
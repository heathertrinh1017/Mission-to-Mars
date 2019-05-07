import sys
import json
import os
from flask import Flask, render_template, redirect
import pymongo
from flask_pymongo import PyMongo
from pymongo import MongoClient
import scrape_mars


sys.setrecursionlimit(2000)

app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"

mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")

# conn = 'mongodb://localhost:27017'
# client = pymongo.MongoClient(conn)
# db = client.mars_db
# collection = db.mars_facts

@app.route("/")
def home():
    dict = mongo.db.dict.find_one()
    return render_template("index.html", dict=dict)


@app.route("/scrape")
def scrape():
    dict = mongo.db.dict
    dict = scrape_mars.scrape()
    mongo.db.collection.update({}, dict, upsert=True)
    return redirect("/")





if __name__ == "__main__":
    app.run(debug=True)

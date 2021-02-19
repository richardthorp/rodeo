import os
from flask_pymongo import PyMongo
from flask import (Flask, flash, render_template,
                   redirect, request, session, url_for)
from flask_paginate import Pagination, get_page_args
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def index():
    test = mongo.db.recipes.find()
    return render_template("index.html", test=test)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)

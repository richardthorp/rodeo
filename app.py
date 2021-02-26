import os
from flask_pymongo import PyMongo
from flask import (Flask, flash, render_template,
                   redirect, request, session, url_for)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_paginate import Pagination, get_page_args
from forms import (Registration_form, Login_form,
                   Search_and_filter_form, Add_recipe_form)
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = Registration_form()
    if form.validate_on_submit():
        existing_user = mongo.db.users.find_one(
                       {"username": request.form.get("username").lower()})
        existing_email = mongo.db.users.find_one(
                       {"email": request.form.get("email").lower()})
        if existing_user:
            flash("Sorry, that username is already taken")
            print("User taken")
        elif existing_email:
            flash("Sorry, that email address already has an account")
            print("Email taken")
        else:
            registration_info = {
                "email": request.form.get('email').lower(),
                "username": request.form.get("username").lower(),
                "password": generate_password_hash(
                            request.form.get("password"))
            }
            mongo.db.users.insert_one(registration_info)
            print("User added")
    else:
        print("NOT VALIDATED")

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = Login_form()
    if form.validate_on_submit():
        email_or_username = request.form.get("email_or_username")
        existing_user = mongo.db.users.find_one(
                        {"$or": [{"username": email_or_username},
                         {"email": email_or_username}]})
        if existing_user:
            if check_password_hash(existing_user["password"],
                                   request.form.get("password")):
                session["username"] = existing_user["username"]
                print("Login successfull")
                return redirect(url_for("index"))

    return render_template("login.html", form=form)


@app.route("/all_recipes")
def all_recipes():
    return render_template("all_recipes.html")


@app.route("/my_recipes", methods=["GET", "POST"])
def my_recipes():
    form = Search_and_filter_form()
    return render_template("my_recipes.html", form=form)


@app.route("/added_recipes")
def added_recipes():
    form = Search_and_filter_form()
    return render_template("added_recipes.html", form=form)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    form = Add_recipe_form()
    if form.validate_on_submit():
        ingredients = []
        quantities = []
        instructions = []
        formatted_recipe = {}
        for item in request.form.items():
            if "ingredient" in item[0]:
                ingredients.append(item)
            elif "quantity" in item[0]:
                quantities.append(item)
            elif "instruction" in item[0]:
                instructions.append(item)
            else:
                formatted_recipe[item[0]] = item[1]
        formatted_recipe["ingredients"] = ingredients
        formatted_recipe["quantities"] = quantities
        formatted_recipe["instructions"] = instructions

        mongo.db.recipes.insert_one(formatted_recipe)
    return render_template("add_recipe.html", form=form)


@app.route("/recipe_page")
def recipe_page():
    recipe = mongo.db.recipes.find_one({"recipe_type": "vegetarian"})
    print(recipe)
    return render_template("recipe_page.html", recipe=recipe)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)

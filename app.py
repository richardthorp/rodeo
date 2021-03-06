import os
from flask_pymongo import PyMongo
from flask import (Flask, flash, render_template,
                   redirect, request, session, url_for)
from bson.objectid import ObjectId
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
            flash("Welcome to Rodeo, " + request.form.get("username") + '!')
            session["username"] = request.form.get("username")
            return redirect(url_for('my_recipes'))

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
            else:
                flash("Login details incorrect, please try again.")
                redirect(url_for('login'))

    return render_template("login.html", form=form)


@app.route("/all_recipes")
def all_recipes():
    recipes = mongo.db.recipes.find()
    return render_template("all_recipes.html", recipes=recipes)


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
        details = {}
        ingredients = []
        quantities = []
        instructions = []
        formatted_recipe = {}
        recipe = dict(request.form)
        details = {key: value for key, value in recipe.items() if
                   "checkbox" in key or "recipe_type" in key}
        for (key, value) in recipe.items():
            if "ingredient" in key:
                ingredients.append(value)
            elif "quantity" in key:
                quantities.append(value)
            elif "instruction" in key:
                instructions.append(value)

        if ingredients[-1] == "":
            ingredients.pop()
            quantities.pop()
        if instructions[-1] == "":
            instructions.pop()

        formatted_recipe = {
            'name': recipe['recipe_name'],
            'feeds': recipe['feeds'],
            'details': details,
            'ingredients': ingredients,
            'quantities': quantities,
            'instructions': instructions,
            'added_by': session['username']
            }
        # If an image file has been sent with form data...
        if request.files['picture_upload']:
            # Remove any special characters from the file name and
            # add username to file name to ensure name is unique
            file_name = "".join(char for char in
                                request.files['picture_upload'].filename
                                if char.isalnum()) + session['username']

            formatted_recipe['image_name'] = file_name
            mongo.save_file(file_name,
                            request.files['picture_upload'])
        mongo.db.recipes.insert_one(formatted_recipe)
    else:
        print("NOT VALID")

    return render_template("add_recipe.html", form=form)


@app.route('/get_image/<image_name>')
def get_image(image_name):
    return mongo.send_file(image_name)


@app.route("/recipe_page/<recipe_id>", methods=["GET", "POST"])
def recipe_page(recipe_id):
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    # Combine ingredients and quantities into one string for
    # easier page rendering
    recipe['ingredients'] = zip(recipe['quantities'], recipe['ingredients'])
    # get all the ratings documents and the number of ratings documents
    recipe_ratings = mongo.db.ratings.find({'recipe_id': recipe_id})
    ratings_count = mongo.db.ratings.count_documents({'recipe_id': recipe_id})
    # Add all the ratings together and then divide by
    # number of ratings (get average)
    ratings_summed = 0
    for rating in recipe_ratings:
        ratings_summed += int(rating['rating'])
    average_rating = ratings_summed / ratings_count

    if recipe['image_name']:
        image_name = recipe['image_name']
    else:
        image_name = url_for('static', '/images/hero.png')
    # If a user is logged in, query db to see if the user has previously
    # 'favourited' the recipe
    logged_in_user = session.get('username')
    favourite = False
    if logged_in_user:
        user_favourite = mongo.db.favourites.find_one({
                                            'recipe_id': recipe_id,
                                            'username': session['username']})
        # if user has recipe saved as a favourite, set 'favourite'
        # variable to True to pass to template.
        if user_favourite:
            favourite = True

    if request.method == 'POST':
        if 'favourite' in request.form:
            if request.form['favourite'] == 'delete_fav':
                mongo.db.favourites.delete_one({
                                        'recipe_id': recipe_id,
                                        'username': session['username']})
            else:
                mongo.db.favourites.insert_one({
                                        'recipe_id': recipe_id,
                                        'username': session['username']})
        if 'rating' in request.form:
            user = session["username"]
            # If user has already rated recipe - delete original rating,
            # then insert new rating
            mongo.db.ratings.delete_one(
                {'recipe_id': recipe_id, 'user': user})
            rating = request.form.get("rating")
            mongo.db.ratings.insert_one({'recipe_id': recipe_id,
                                         'user': user,
                                         'rating': rating})
        return redirect(url_for('recipe_page', recipe_id=recipe_id))

    return render_template("recipe_page.html", recipe=recipe,
                           average_rating=round(average_rating),
                           favourite=favourite, image_name=image_name)


@app.route("/logout")
def log_out():
    session.pop("username")
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)

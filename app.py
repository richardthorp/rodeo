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
    # Get top 3 recipes with highest average_rating
    recipes = recipes = mongo.db.recipes.find().sort(
                        'average_rating', -1).limit(3)
    return render_template("index.html", recipes=recipes)


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
                "username": request.form.get("username"),
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
                print("Login successfull", session['username'])
                return redirect(url_for("index"))
            else:
                flash("Login details incorrect, please try again.")
                redirect(url_for('login'))

    return render_template("login.html", form=form)


@app.route("/all_recipes", methods=['GET', 'POST'])
def all_recipes():
    form = Search_and_filter_form()
    recipes = mongo.db.recipes.find()
    # If user uses search or filter form
    if form.validate_on_submit():
        form_data = (dict(request.form))
        
        # Create an empty dictionary to populate with a search query
        search_terms = {}

        # Remove csrf_token, search_submit and filter_submit
        # from the returned form data
        form_data.pop('csrf_token')
        if form_data.get('search_submit'):
            form_data.pop('search_submit')
        if form_data.get('filter_submit'):
            form_data.pop('filter_submit')

        # If user entered search terms, add text search to search_terms dict
        if form_data['search'] != "":
            search_terms = {"$text": {"$search": form_data['search']}}
        # Remove 'search' item form_data dict
        form_data.pop('search')

        # If user has selected a recipe_type that isn't 'All', add recipe_type
        # query to the search terms dict
        if form_data['recipe_type'] != 'All':
            search_terms['details.recipe_type'] = form_data['recipe_type']
        # Remove 'recipe_type' item from form data dict.
        form_data.pop('recipe_type')

        # Add any selected checkboxes to the search_terms dict
        for key, value in form_data.items():
            search_terms['details.' + key] = value

        # Finally, query the db with the formatted search_terms dict
        recipes = mongo.db.recipes.find(search_terms)
    else:
        print('NOT VALID', form.errors)

    return render_template("all_recipes.html", form=form, recipes=recipes)


@app.route("/my_recipes", methods=["GET", "POST"])
def my_recipes():
    form = Search_and_filter_form()
    recipes = mongo.db.recipes.find({"favourites": session['username']})
    return render_template("my_recipes.html", form=form, recipes=recipes)


@app.route("/added_recipes")
def added_recipes():
    form = Search_and_filter_form()
    recipes = mongo.db.recipes.find({"added_by": session['username']})
    return render_template("added_recipes.html", form=form, recipes=recipes)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    form = Add_recipe_form()

    if form.validate_on_submit():
        details = {}
        ingredients = []
        instructions = []
        formatted_recipe = {}
        recipe = dict(request.form)
        details = {key: value for key, value in recipe.items() if
                   "checkbox" in key or "recipe_type" in key}
        for (key, value) in recipe.items():
            if "ingredient" in key and value != "":
                ingredients.append(value.strip())
            elif "instruction" in key and value != "":
                instructions.append(value.strip())

        if ingredients[-1] == "":
            ingredients.pop()
        if instructions[-1] == "":
            instructions.pop()

        formatted_recipe = {
            'name': recipe['recipe_name'].strip(),
            'feeds': recipe['feeds'],
            'details': details,
            'ingredients': ingredients,
            'instructions': instructions,
            'added_by': session['username'],
            'ratings': {},
            'favourites': []
            }
        # If an image file has been sent with form data...
        if request.files['picture_upload']:
            # Remove any special characters from the file name and
            # add username to file name to ensure name is unique
            file_name = "".join(char for char in
                                request.files['picture_upload'].filename
                                if char.isalnum()) + session['username']

            mongo.save_file(file_name,
                            request.files['picture_upload'])
            formatted_recipe['image_name'] = file_name
        else:
            formatted_recipe['image_name'] = 'defaultrecipeimagepngRodeo'
        mongo.db.recipes.insert_one(formatted_recipe)
    else:
        print("NOT VALID", form.errors)

    return render_template("add_recipe.html", form=form)


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    print('DELETE BUTTON CLICKED')
    return redirect(url_for('my_recipes'))


@app.route('/edit_recipe/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    form = Add_recipe_form()
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    if request.method == 'POST':
        print('TESTER', request.form)
    if form.validate_on_submit():
        print(request.form)
        details = {}
        ingredients = []
        instructions = []
        formatted_recipe = {}
        recipe = dict(request.form)
        details = {key: value for key, value in recipe.items() if
                   "checkbox" in key or "recipe_type" in key}
        for (key, value) in recipe.items():
            if "ingredient" in key and value != "":
                ingredients.append(value.strip())
            elif "instruction" in key and value != "":
                instructions.append(value.strip())

        formatted_recipe = {
            'name': recipe['recipe_name'].strip(),
            'feeds': recipe['feeds'],
            'details': details,
            'ingredients': ingredients,
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

            mongo.save_file(file_name,
                            request.files['picture_upload'])
            formatted_recipe['image_name'] = file_name
        else:
            formatted_recipe['image_name'] = 'defaultrecipeimagepngRodeo'
        mongo.db.recipes.update_one({'_id': ObjectId(recipe_id)},
                                    {'$set': formatted_recipe})
        print(formatted_recipe)
        return redirect(url_for('recipe_page', recipe_id=recipe_id))
    else:
        print('ERROR VALIDATING', form.errors)
    return render_template('edit_recipe.html', form=form, recipe=recipe)


@app.route('/get_image/<image_name>')
def get_image(image_name):
    return mongo.send_file(image_name)


@app.route("/recipe_page/<recipe_id>", methods=["GET", "POST"])
def recipe_page(recipe_id):
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})

    average_rating = get_average_rating(recipe_id)
    mongo.db.recipes.update_one({'_id': ObjectId(recipe_id)},
                                {'$set': {'average_rating': average_rating}})
    # If an existing user rating for the recipe exists, get the user rating
    # to render on the page
    user_rating = 0
    if 'username' in session:
        if session['username'] in recipe['ratings']:
            user_rating = int(recipe['ratings'][session['username']])

    # NEED TO LOOK INTO BEST WAY TO SET DEFAULT ~~~~~~~~~~~~~~~~~~~~~
    if recipe['image_name']:
        image_name = recipe['image_name']
    else:
        image_name = url_for('static', filename='/images/hero.png')

    if request.method == 'POST':
        # Find the respective recipe, and within the ratings field set
        # username and user rating
        mongo.db.recipes.update_one({'_id': ObjectId(recipe_id)}, {'$set':
                                    {'ratings.' + session['username']:
                                        request.form.get('rating')}})

        return redirect(url_for('recipe_page', recipe_id=recipe_id))

    return render_template("recipe_page.html", recipe=recipe,
                           average_rating=round(average_rating),
                           image_name=image_name, user_rating=user_rating)


def get_average_rating(recipe_id):
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    # Find out how many ratings the recipe has
    ratings_count = len(recipe['ratings'].values())

    # If the recipe has ratings, add them together and divide by
    # ratings count to find average rating
    if ratings_count:
        ratings_summed = 0
        for rating in recipe['ratings'].values():
            ratings_summed += int(rating)
        average_rating = ratings_summed / ratings_count
    else:
        average_rating = 0

    return average_rating


@app.route('/toggle_favourite/<recipe_id>/<return_page>',
           methods=['GET', 'POST'])
def toggle_favourite(**kwargs):
    recipe_id = kwargs['recipe_id']
    return_page = kwargs['return_page']
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})

    if session['username'] in recipe['favourites']:
        mongo.db.recipes.update_one(
                        {'_id': ObjectId(recipe_id)},
                        {'$pull': {'favourites': session['username']}})
    else:
        mongo.db.recipes.update_one(
                        {'_id': ObjectId(recipe_id)},
                        {'$push': {'favourites': session['username']}})

    return redirect(url_for(return_page, recipe_id=recipe_id))


@app.route("/logout")
def log_out():
    session.pop("username")
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)

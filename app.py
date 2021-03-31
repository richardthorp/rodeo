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
    if request.method == 'POST':
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
                flash("Welcome to Rodeo, " +
                      request.form.get("username") + '!')
                session["username"] = request.form.get("username")
                return redirect(url_for('my_recipes'))

        elif 'confirm_password' in form.errors:
            flash('Please make sure the password fields match')
        else:
            flash('Sorry, there has been an error. Please try again.')

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
                flash('Welcome, ' + session['username'] + '!')
                return redirect(url_for("my_recipes"))
        else:
            flash("Login details incorrect, please try again.")
            return redirect(url_for('login'))

    return render_template("login.html", form=form)


@app.route("/all_recipes", methods=['GET', 'POST'])
def all_recipes():
    form = Search_and_filter_form()
    recipes = mongo.db.recipes.find()
    filters = False
    # If user uses search and filter form
    if form.validate_on_submit():
        form_data = (dict(request.form))
        recipes = search_and_filter(form_data, 'all_recipes')
        filters = True
    else:
        print('NOT VALID', form.errors)

    return render_template("all_recipes.html", form=form, recipes=recipes,
                           filters=filters)


@app.route("/my_recipes", methods=["GET", "POST"])
def my_recipes():
    if session.get('username'):
        form = Search_and_filter_form()
        recipes = mongo.db.recipes.find({"favourites": session['username']})
        filters = False
        if form.validate_on_submit():
            form_data = (dict(request.form))
            recipes = search_and_filter(form_data, 'favourite_recipes')
            filters = True

        return render_template("my_recipes.html", form=form, recipes=recipes,
                               filters=filters)
    else:
        flash('Please log in to add and favourite recipes')
        return redirect(url_for('login'))


@app.route("/added_recipes", methods=["GET", "POST"])
def added_recipes():
    if session.get('username'):
        form = Search_and_filter_form()
        recipes = mongo.db.recipes.find({"added_by": session['username']})
        filters = False

        if form.validate_on_submit():
            form_data = (dict(request.form))
            recipes = search_and_filter(form_data, 'added_recipes')
            filters = True
        return render_template("added_recipes.html", form=form,
                               recipes=recipes, filters=filters)
    else:
        flash('Please log in to add and favourite recipes')
        return redirect(url_for('login'))


def search_and_filter(form_data, page):
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
    if page == 'favourite_recipes':
        search_terms.update({"favourites": session['username']})
    if page == 'added_recipes':
        search_terms.update({"added_by": session['username']})

    # Finally, query the db with the formatted search_terms dict
    return mongo.db.recipes.find(search_terms)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if not session.get('username'):
        flash('Please log in to add and favourite recipes')
        return redirect(url_for('login'))
    else:
        form = Add_recipe_form()
        if request.method == 'POST':
            if form.validate_on_submit():
                form_data_dict = dict(request.form)
                formatted_recipe = format_recipe_data(form_data_dict)

                # If an image file has been sent with form data...
                if request.files['picture_upload']:
                    # Remove any special characters from the file name and
                    # add user _id to file name to ensure name is unique
                    user = mongo.db.users.find_one({'username': session['username']})
                    user_id = str(user['_id'])
                    file_name = "".join(char for char in
                                        request.files['picture_upload'].filename
                                        if char.isalnum()) + user_id

                    mongo.save_file(file_name,
                                    request.files['picture_upload'])
                    formatted_recipe['image_name'] = file_name
                else:
                    formatted_recipe['image_name'] = 'defaultrecipeimagepngRodeo'

                # Insert recipe to DB
                mongo.db.recipes.insert_one(formatted_recipe)
                flash('Recipe added! Thank you!')
                return redirect(url_for('added_recipes'))

            # Invalid form...
            else:
                flash('''Sorry, there was an issue with the form data.
                    Please try again''')
                print("NOT VALID", form.errors)
        else:
            return render_template("add_recipe.html", form=form)


@app.route('/edit_recipe/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    # User not logged in...
    if not session.get('username'):
        flash('Please log in to add and favourite recipes')
        return redirect(url_for('login'))
    else:
        form = Add_recipe_form()
        recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
        if request.method == 'POST':
            if form.validate_on_submit():
                form_data_dict = dict(request.form)
                formatted_recipe = format_recipe_data(form_data_dict)
                # If the 'picture_upload' input has been used, there is no
                # existing image in the database to remove, so just format the
                # name upload to db
                print(form_data_dict)
                if request.files.get('picture_upload'):
                    # Remove any special characters from the file name and
                    # add user _id to file name to ensure name is unique
                    user = mongo.db.users.find_one({
                                        'username': session['username']})
                    user_id = str(user['_id'])
                    file_name = "".join(char for char in
                                        request.files['picture_upload'].filename
                                        if char.isalnum()) + user_id

                    mongo.save_file(file_name,
                                    request.files['picture_upload'])
                    formatted_recipe['image_name'] = file_name

                # If the new_picture_upload input has been used, this means the
                # image is to replace an existing user uploaded image, so find
                # the original image and delete before formatting new image
                # name and uploading to db
                elif request.files.get('new_picture_upload') and form_data_dict['image_options'] == 'new_image':
                    # Find image data in fs.files using recipe image_name
                    db_image = mongo.db.fs.files.find_one({
                        'filename': recipe['image_name']})

                    # Find the image data in the fs.chunks collection and delete
                    # using _id of file found in query above
                    mongo.db.fs.chunks.delete_one({'files_id': ObjectId(db_image['_id'])})

                    # Then delete image file meta data from fs.files
                    mongo.db.fs.files.delete_one({'filename': recipe['image_name']})

                    user = mongo.db.users.find_one({
                                        'username': session['username']})
                    user_id = str(user['_id'])
                    file_name = "".join(char for char in
                                        request.files['new_picture_upload'].filename
                                        if char.isalnum()) + user_id
                    mongo.save_file(file_name, request.files['new_picture_upload'])
                    formatted_recipe['image_name'] = file_name

                # User had uploaded an image but now wants to use the default image - 
                # Delete existing image data from db and set new image to default
                elif form_data_dict['image_options'] == 'default_image':
                    db_image = mongo.db.fs.files.find_one({
                        'filename': recipe['image_name']})

                    # Find the image data in the fs.chunks collection and delete
                    # using _id of file found in query above
                    mongo.db.fs.chunks.delete_many({'files_id': ObjectId(db_image['_id'])})

                    # Then delete image file meta data from fs.files
                    mongo.db.fs.files.delete_one({'filename': recipe['image_name']})
                    formatted_recipe['image_name'] = 'defaultrecipeimagepngRodeo'

                print(formatted_recipe)
                # Update recipe in DB
                mongo.db.recipes.update_one({'_id': ObjectId(recipe_id)},
                                            {'$set': formatted_recipe})
                return redirect(url_for('recipe_page', recipe_id=recipe_id))
            # Invalid form...
            else:
                flash('''Sorry, there was an issue with the form data.
                    Please try again''')
                print("NOT VALID", form.errors)
        return render_template('edit_recipe.html', form=form, recipe=recipe)


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    # If recipe image is default, just delete recipe info from db
    if recipe['image_name'] == 'defaultrecipeimagepngRodeo':
        mongo.db.recipes.delete_one({'_id': ObjectId(recipe_id)})
        flash('Recipe Deleted')
        return redirect(url_for('added_recipes'))
    else:
        # Find image data in fs.files using recipe image_name
        db_image = mongo.db.fs.files.find_one({
                        'filename': recipe['image_name']})

        # Find the image data in the fs.chunks collection and delete
        # using _id of file found in query above
        mongo.db.fs.chunks.delete_one({'files_id': ObjectId(db_image['_id'])})

        # Then delete image file meta data from fs.files
        mongo.db.fs.files.delete_one({'filename': recipe['image_name']})

        # Then delete recipe data
        mongo.db.recipes.delete_one({'_id': ObjectId(recipe_id)})
        flash('Recipe Deleted')
        return redirect(url_for('added_recipes'))


@app.route('/get_image/<image_name>')
def get_image(image_name):
    return mongo.send_file(image_name)


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
        flash('Recipe removed from your favourites')
    else:
        mongo.db.recipes.update_one(
                        {'_id': ObjectId(recipe_id)},
                        {'$push': {'favourites': session['username']}})
        flash('Recipe added to your favourites')
    return redirect(url_for(return_page, recipe_id=recipe_id))


@app.route("/logout")
def log_out():
    session.pop("username")
    flash('Log out successful, see you soon!')
    return redirect(url_for('index'))


@app.route("/recipe_page/<recipe_id>", methods=["GET", "POST"])
def recipe_page(recipe_id):
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
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
        # Calculate new average_rating and update in the db
        average_rating = get_average_rating(recipe_id)
        mongo.db.recipes.update_one({'_id': ObjectId(recipe_id)},
                                    {'$set': {'average_rating': average_rating}})

        return redirect(url_for('recipe_page', recipe_id=recipe_id))

    return render_template("recipe_page.html", recipe=recipe,
                           image_name=image_name, user_rating=user_rating)


def format_recipe_data(form_data_dict):
    details = {}
    ingredients = []
    instructions = []
    formatted_recipe = {}
    details = {key: value for key, value in form_data_dict.items() if
                "checkbox" in key or "recipe_type" in key}
    for (key, value) in form_data_dict.items():
        if "ingredient" in key and value != "":
            ingredients.append(value.strip())
        elif "instruction" in key and value != "":
            instructions.append(value.strip())

    if ingredients[-1] == "":
        ingredients.pop()
    if instructions[-1] == "":
        instructions.pop()

    formatted_recipe = {
        'name': form_data_dict['recipe_name'].strip(),
        'feeds': form_data_dict['feeds'],
        'details': details,
        'ingredients': ingredients,
        'instructions': instructions,
        'added_by': session['username'],
        'ratings': {},
        'average_rating': 0,
        'favourites': []
        }
    return formatted_recipe


def get_average_rating(recipe_id):
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    # Find out how many ratings the recipe has
    ratings_count = len(recipe['ratings'])

    # If the recipe has ratings, add them together and divide by
    # ratings count to find average rating
    if ratings_count:
        ratings_summed = 0
        for rating in recipe['ratings'].values():
            ratings_summed += int(rating)
        average_rating = ratings_summed / ratings_count
    else:
        average_rating = 0
    # Round the rating to the nearest .5
    return round(average_rating * 2) / 2


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)

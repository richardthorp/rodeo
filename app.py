import os
import math
from flask_pymongo import PyMongo
from flask import (Flask, flash, render_template,
                   redirect, request, session, url_for)
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from forms import (Registration_form, Login_form,
                   Search_and_filter_form, Add_recipe_form)
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config['MAX_CONTENT_LENGTH'] = 1.2 * 1024 * 1024

mongo = PyMongo(app)


@app.route("/index")
@app.route("/")
def index():
    # Get top 3 recipes with highest average_rating
    recipes = recipes = mongo.db.recipes.find().sort(
                        'average_rating', -1).limit(4)
    return render_template("index.html", recipes=recipes)


@app.route("/register", methods=["GET", "POST"])
def register():
    # if user is already logged in, redirect to my_recipes route
    if session.get('username'):
        return redirect(url_for('my_recipes'))

    form = Registration_form()
    if request.method == 'POST':
        if form.validate_on_submit():
            # Check the database for any existing users that match either the
            # username or email form data
            existing_user = mongo.db.users.find_one(
                        {"username": request.form.get("username").lower()})
            existing_email = mongo.db.users.find_one(
                        {"email": request.form.get("email").lower()})
            # If username or email already exist, flash message to say which
            # field is the problem
            if existing_user:
                flash("Sorry, that username is already taken")
            elif existing_email:
                flash("Sorry, that email address already has an account")
            # All details on the form are valid, add user to DB.
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

        # FORM NOT VALIDATED
        elif 'confirm_password' in form.errors:  # Miss-matched passwords
            flash('Please make sure the password fields match')
        else:  # There is another issue with the form data
            flash('Sorry, there has been an error. Please try again.')

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    # if user is already logged in, redirect to my_recipes route
    if session.get('username'):
        return redirect(url_for('my_recipes'))

    form = Login_form()
    if request.method == 'POST':
        if form.validate_on_submit():
            email_or_username = request.form.get("email_or_username").lower()
            # Look in DB for either a username or email that matches
            # form email_or_username data
            existing_user = mongo.db.users.find_one(
                            {"$or": [{"username": email_or_username},
                                     {"email": email_or_username}]})
            if existing_user:  # User exists in the DB - check the passwords
                if check_password_hash(existing_user["password"],
                                       request.form.get("password")):
                    session["username"] = existing_user["username"]
                    flash('Welcome, ' + session['username'] + '!')
                    return redirect(url_for("my_recipes"))
                else:  # Password is incorrect
                    flash("Login details incorrect, please try again.")
                    return redirect(url_for('login'))
            else:  # No matching user found on DB
                flash("Login details incorrect, please try again.")
                return redirect(url_for('login'))

    return render_template("login.html", form=form)


# This function queries the database for all_recipes, my_recipes, added_recipes
# and search_results route functions as well as generating the pagination links
# for each route.
def get_recipes_paginated(return_route, page, sort_by, **kwargs):
    # If this function is called in the search_results route, the return_page
    # var needs to be passed in as a kwarg to tell the pagination links which
    # template is being rendered in the return statement of the search_results
    # route
    if return_route == 'search_results':
        db_query = session['search_terms']
        return_page = kwargs.get('return_page')
        next_page = url_for(return_route, page=str(page + 1),
                            return_page=return_page, sort_by=sort_by)
        prev_page = url_for(return_route, page=str(page - 1),
                            return_page=return_page, sort_by=sort_by)
    # Otherwise, the route functions have the render_template argument hard
    # coded in the routes
    else:
        next_page = url_for(return_route, page=str(page + 1), sort_by=sort_by)
        prev_page = url_for(return_route, page=str(page - 1), sort_by=sort_by)

    if return_route == 'all_recipes':
        db_query = {}
    elif return_route == 'my_recipes':
        db_query = {'favourites': session['username']}
    elif return_route == 'added_recipes':
        db_query = {'added_by': session['username']}

    # Query DB using the dict created above
    if page == 1:  # This is page one, fetch the first 12 recipes
        recipes = mongo.db.recipes.find(db_query).sort(
            [(sort_by, -1), ('_id', -1)]).limit(12)

    else:  # This is not page one, skip forwards by required amount
        recipes = mongo.db.recipes.find(db_query).sort(
            [(sort_by, -1), ('_id', -1)]).skip(
                (page - 1) * 12).limit(12)

    recipe_count = mongo.db.recipes.count_documents(db_query)
    max_page = math.ceil(recipe_count / 12)

    return recipes, next_page, prev_page, recipe_count, max_page


@app.route("/all_recipes", methods=['GET', 'POST'])
def all_recipes():
    form = Search_and_filter_form()
    # If no page arg sent to function, this is page 1
    page = request.args.get('page', 1, type=int)
    # If no sort_by arg sent to function, sort by rating
    sort_by = request.args.get('sort_by', 'average_rating', type=str)
    # Call get_recipes_paginated() to fetch recipes from DB and generate
    # pagination links
    (recipes, next_page, prev_page, recipe_count,
        max_page) = get_recipes_paginated('all_recipes', page, sort_by)

    return render_template("all_recipes.html", form=form, recipes=recipes,
                           next_page=next_page, prev_page=prev_page,
                           max_page=max_page, page=page,
                           recipe_count=recipe_count, sort_by=sort_by)


# This route function is the same as the all_recipes route above
@app.route("/my_recipes", methods=["GET", "POST"])
def my_recipes():
    # If user not logged in, redirect to login route
    if not session.get('username'):
        flash('Please log in to add and favourite recipes')
        return redirect(url_for('login'))

    form = Search_and_filter_form()
    page = request.args.get('page', 1, type=int)
    sort_by = request.args.get('sort_by', 'average_rating', type=str)

    (recipes, next_page, prev_page, recipe_count,
        max_page) = get_recipes_paginated('my_recipes', page, sort_by)

    return render_template("my_recipes.html", form=form, recipes=recipes,
                           next_page=next_page, prev_page=prev_page,
                           max_page=max_page, page=page,
                           recipe_count=recipe_count, sort_by=sort_by)


# This route function is the same as the all_recipes route above
@app.route("/added_recipes", methods=["GET", "POST"])
def added_recipes():
    # If user not logged in, redirect to login route
    if not session.get('username'):
        flash('Please log in to add and favourite recipes')
        return redirect(url_for('login'))

    form = Search_and_filter_form()
    page = request.args.get('page', 1, type=int)
    sort_by = request.args.get('sort_by', 'average_rating', type=str)

    (recipes, next_page, prev_page, recipe_count,
        max_page) = get_recipes_paginated('added_recipes', page, sort_by)

    return render_template("added_recipes.html", form=form, recipes=recipes,
                           next_page=next_page, prev_page=prev_page,
                           max_page=max_page, page=page,
                           recipe_count=recipe_count, sort_by=sort_by)


# search_results route used to provide results for all pages that contain
# search functionality. The route works in the same way as all_recipes,
# my_recipes and added_recipes routes, but the DB query is saved as a session
# variable having been created in the create_query_dict function. This allows
# pagination to work with the search results.
@app.route('/search_results', methods=["GET", "POST"])
def search_results():
    filters = True  # Used to toggle 'clear_search' link in templates
    form = Search_and_filter_form()
    page = request.args.get('page', 1, type=int)
    sort_by = request.args.get('sort_by', 'average_rating', type=str)
    # The return_page variable is required to instruct this route which
    # template to display the results in.
    return_page = request.args.get('return_page', type=str)

    # If data has been sent via the Search_and_filter_form, update the
    # search_terms variable in session.
    if request.method == 'POST':
        form_data = (dict(request.form))
        session['search_terms'] = create_query_dict(form_data, return_page)

    (recipes, next_page, prev_page, recipe_count,
        max_page) = get_recipes_paginated('search_results', page, sort_by,
                                          return_page=return_page)

    # If the user searched using the search box, save the search words in a var
    # to be able to render them in the search box if pagination links are used
    if session['search_terms'].get('$text'):
        search_words = session['search_terms'].get('$text').get('$search')
    else:
        search_words = ""

    return render_template(return_page + ".html", recipes=recipes, form=form,
                           page=page, next_page=next_page, prev_page=prev_page,
                           max_page=max_page, filters=filters,
                           recipe_count=recipe_count, sort_by=sort_by,
                           search_words=search_words)


def create_query_dict(form_data, page):
    # Create an empty dictionary to populate with a search query
    search_terms = {}
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
    if page == 'my_recipes':
        search_terms.update({"favourites": session['username']})
    if page == 'added_recipes':
        search_terms.update({"added_by": session['username']})

    # Return dictionary of search terms
    return search_terms


# Clear out any search terms from the session variable and redirect to the
# page that called the function
@app.route('/clear_search/<return_page>')
def clear_search(return_page):
    session['search_terms'] = {}
    return redirect(url_for(return_page))


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    # User not logged in - redirect to login route
    if not session.get('username'):
        flash('Please log in to add and favourite recipes')
        return redirect(url_for('login'))

    form = Add_recipe_form()
    if request.method == 'POST':
        if form.validate_on_submit():
            form_data_dict = dict(request.form)
            formatted_recipe = format_recipe_data(form_data_dict)

            # If an image file has been sent with form data...
            if request.files['picture_upload']:
                # Remove any special characters from the file name and
                # add user _id to file name to ensure name is unique
                user = mongo.db.users.find_one({
                                'username': session['username']})
                user_id = str(user['_id'])
                file_name = "".join(char for char in
                                    request.files['picture_upload'].filename
                                    if char.isalnum()) + user_id
                # Add image to DB
                mongo.save_file(file_name,
                                request.files['picture_upload'])
                # Set the image name in the recipe dict
                formatted_recipe['image_name'] = file_name

            # No image was sent with the form, use the locally
            # stored default image
            else:
                formatted_recipe['image_name'] = 'default-image'

            # Add 5 x 3 star ratings to level out average ratings
            formatted_recipe['ratings'] = {"a": 3,
                                           "b": 3,
                                           "c": 3,
                                           "d": 3,
                                           "e": 3}

            # Insert recipe to DB
            recipe_id = mongo.db.recipes.insert_one(formatted_recipe)
            flash('Recipe added! Thank you!')
            return redirect(url_for('recipe_page',
                                    recipe_id=recipe_id.inserted_id))

        else:  # Invalid form...
            flash('''Sorry, there was an issue with the form data.
                    Please try again''')
            return render_template("add_recipe.html", form=form)
    else:
        return render_template("add_recipe.html", form=form)


@app.route('/edit_recipe/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    # User not logged in...
    if not session.get('username'):
        flash('Please log in to add and favourite recipes')
        return redirect(url_for('login'))

    form = Add_recipe_form()
    # Get the existing recipe data to render to the page
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    if request.method == 'POST':
        if form.validate_on_submit():
            form_data_dict = dict(request.form)
            formatted_recipe = format_recipe_data(form_data_dict)
            # If 'picture_upload' is truthy in request.files, we know there
            # is no existing image in the database to remove because that input
            # is only shown in the template when image.name == 'default-image',
            # so just format the image name and upload file to DB
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

            # If image_options == new_image, the image sent with the form is to
            # replace an existing user uploaded image, so find the original
            # image in the DB and delete before formatting new image name and
            # uploading to DB.
            elif (form_data_dict.get('image_options') == 'new_image'):
                # Call delete_image to remove image data from db
                delete_image(recipe['image_name'])
                # find the user _id to append to the image name
                user = mongo.db.users.find_one({
                                    'username': session['username']})
                user_id = str(user['_id'])
                # make sure only alphanumeric characters are in the file name,
                # and then add user _id to file name to make unique
                file_name = "".join(char for char in request.files[
                                        'new_picture_upload'].filename
                                    if char.isalnum()) + user_id
                mongo.save_file(file_name, request.files['new_picture_upload'])
                formatted_recipe['image_name'] = file_name

            # If image_options == default_image, the user had uploaded an image
            # but now wants to use the default image. Delete existing image
            # data from db and set new image name to 'default-image'.
            elif form_data_dict.get('image_options') == 'default_image':
                # Call delete_image to remove image data from db
                delete_image(recipe['image_name'])
                # Set recipe image name to default image
                formatted_recipe['image_name'] = 'default-image'

            # Update recipe in DB
            mongo.db.recipes.update_one({'_id': ObjectId(recipe_id)},
                                        {'$set': formatted_recipe})
            return redirect(url_for('recipe_page', recipe_id=recipe_id))

        else:  # Invalid form...
            flash('''
                Sorry, there was an issue with the form data.
                Please try again
                ''')
    return render_template('edit_recipe.html', form=form, recipe=recipe)


# This function takes raw form data sent add_recipe or edit_recipe and formats
# it before being inserted into DB.
def format_recipe_data(form_data_dict):
    details = {}
    ingredients = []
    instructions = []
    formatted_recipe = {}
    details = {key: value for key, value in form_data_dict.items() if
               "checkbox" in key or "recipe_type" in key}
    # Remove any leading or trailing whitespace from ingredient
    # and instruction inputs
    for (key, value) in form_data_dict.items():
        if "ingredient" in key and value != "":
            ingredients.append(value.strip())
        elif "instruction" in key and value != "":
            instructions.append(value.strip())

    # Remove any empty text fields that could be sent with form data
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
        'average_rating': 3,
        'favourites': []
        }
    return formatted_recipe


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    page = request.args.get('page', 1, type=int)
    filters = request.args.get('filters')
    sort_by = request.args.get('sort_by', 'average_rating', type=str)
    # Find the recipe to delete in the DB
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})

    # Recipe has a user uploaded image
    if recipe['image_name'] != 'default-image':
        # Call delete_image() to remove image data from db
        delete_image(recipe['image_name'])

    # Delete recipe from DB
    mongo.db.recipes.delete_one({'_id': ObjectId(recipe_id)})
    flash('Recipe Deleted')
    if filters:
        return redirect(url_for('search_results', return_page='added_recipes',
                                page=page, sort_by=sort_by))
    else:
        return redirect(url_for('added_recipes', page=page, sort_by=sort_by))


def delete_image(image_name):
    # Find image data in fs.files using recipe image_name
    db_image = mongo.db.fs.files.find_one({
                    'filename': image_name})

    # Find the image data in the fs.chunks collection and delete
    # using _id of file found in query above
    mongo.db.fs.chunks.delete_one({'files_id': ObjectId(db_image['_id'])})

    # Then delete image file meta data from fs.files
    mongo.db.fs.files.delete_one({'filename': image_name})


# This function is called in the templates if the recipe image name
# is not 'default-image'.
@app.route('/get_image/<image_name>')
def get_image(image_name):
    return mongo.send_file(image_name)


@app.route('/toggle_favourite', methods=['GET', 'POST'])
def toggle_favourite():
    # These variables are collected to ensure the user is returned to
    # the page that they 'toggled' the favourite recipe on, along with any
    # specific search terms.
    page = request.args.get('page', 1, type=int)
    recipe_id = request.args.get('recipe_id')
    return_page = request.args.get('return_page')
    filters = request.args.get('filters')
    back_link = request.args.get('back_link')
    back_link_text = request.args.get('back_link_text')
    sort_by = request.args.get('sort_by', 'average_rating', type=str)
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})

    # User has previously added recipe to favourites, so remove recipe
    # from favourites
    if session['username'] in recipe['favourites']:
        mongo.db.recipes.update_one(
                        {'_id': ObjectId(recipe_id)},
                        {'$pull': {'favourites': session['username']}})
        flash('Recipe removed from your favourites')
    # User has not previously added recipe to favourites, so add recipe
    # to favourites
    else:
        mongo.db.recipes.update_one(
                        {'_id': ObjectId(recipe_id)},
                        {'$push': {'favourites': session['username']}})
        flash('Recipe added to your favourites')

    # If called from recipe_page, return to the recipe page with all the data
    # required to allow user to keep browsing search results if they use the
    # 'back to...' link
    if return_page == 'recipe_page':
        return redirect(url_for('recipe_page', recipe_id=recipe_id,
                                sort_by=sort_by, back_link=back_link,
                                back_link_text=back_link_text,
                                filters=filters))
    # If the return page isn't recipe_page and filters is truthy, the function
    # has been called whilst browsing search results
    elif return_page != 'recipe_page' and filters:
        return redirect(url_for('search_results', page=page,
                                return_page=return_page, sort_by=sort_by))
    # Otherwise, return to original page with relevant args
    else:
        return redirect(url_for(return_page, page=page, sort_by=sort_by))


@app.route("/logout")
def log_out():
    session.clear()  # Clear out any session data
    flash('Log out successful, see you soon!')
    return redirect(url_for('index'))


@app.route("/recipe_page/<recipe_id>", methods=["GET", "POST"])
def recipe_page(recipe_id):
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    # These variables are to pass to the 'back to...' link
    page = request.args.get('page', 1, type=int)
    # recipe_id = request.args.get('recipe_id')
    recipe_id = recipe['_id']
    back_link = request.args.get('back_link')
    back_link_text = request.args.get('back_link_text')
    filters = request.args.get('filters')
    sort_by = request.args.get('sort_by', 'average_rating', type=str)

    user_rating = 0
    # If the user is logged in, see if they have aleady rated this recipe.
    # If so, save the rating to a variable to render to the page
    if 'username' in session:
        if session['username'] in recipe['ratings']:
            user_rating = int(recipe['ratings'][session['username']])

    # If method is POST, the user has submitted a recipe rating
    if request.method == 'POST':
        # Find the respective recipe, and within the ratings dict set
        # username and user rating
        user_rating = request.form.get('rating', 0, type=int)
        mongo.db.recipes.update_one({'_id': ObjectId(recipe_id)}, {'$set':
                                    {'ratings.' + session['username']:
                                        user_rating}})
        # Calculate new average_rating and update in the db
        average_rating = get_average_rating(recipe_id)
        mongo.db.recipes.update_one({'_id': ObjectId(recipe_id)},
                                    {'$set': {
                                        'average_rating': average_rating}})
        flash('Thank you for your rating!')

        return redirect(url_for('recipe_page', recipe_id=recipe_id,
                                sort_by=sort_by, filters=filters,
                                back_link=back_link,
                                back_link_text=back_link_text))

    return render_template("recipe_page.html", recipe=recipe,
                           user_rating=user_rating, page=page, filters=filters,
                           sort_by=sort_by, back_link=back_link,
                           max_page=1, back_link_text=back_link_text)


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


@app.errorhandler(404)
def page_not_found(err):
    return render_template("404.html")


@app.errorhandler(500)
def server_error(err):
    return render_template("500.html")


# This error is for a request object that exceeds the file size
# limit set in the MAX_CONTENT_LENGTH config var in the top of this file
@app.errorhandler(413)
def request_entity_too_big(err):
    flash("The image file was too big, please use a different file.")
    return redirect(url_for('added_recipes'))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)

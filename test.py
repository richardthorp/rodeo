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

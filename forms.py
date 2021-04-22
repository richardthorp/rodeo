from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField,
                     SubmitField, RadioField, BooleanField, TextAreaField,
                     IntegerField, FileField)
from flask_wtf.file import FileAllowed
from wtforms.validators import InputRequired, Length, Email, EqualTo
from wtforms.fields.html5 import EmailField


# FieldsRequiredForm class found at
# https://github.com/wtforms/wtforms/issues/477
# The class is used to fix a bug whereby the required
# attribute is not set on RadioField inputs
class FieldsRequiredForm(FlaskForm):
    class Meta:
        def render_field(self, field, render_kw):
            if field.type == "_Option":
                render_kw.setdefault("required", True)
            return super().render_field(field, render_kw)


class Registration_form(FlaskForm):
    email = EmailField("Email Address",
                       validators=[Email(),
                                   InputRequired()],
                       render_kw={"placeholder": "Email Address"})
    username = StringField("Username",
                           validators=[InputRequired(), Length(min=4, max=25)],
                           render_kw={"placeholder": "Choose Username",
                                      "minlength": "4",
                                      "maxlength": "25"})
    password = PasswordField("Password",
                             validators=[InputRequired(), Length(min=8)],
                             render_kw={"placeholder": "Choose Password",
                                        "minlength": "8"})
    confirm_password = PasswordField("Confirm Password", validators=[
                                     InputRequired(), EqualTo('password')],
                                     render_kw={"placeholder":
                                                "Retype Password"})
    submit = SubmitField("Register")


class Login_form(FlaskForm):
    email_or_username = StringField("Email Address",
                                    validators=[InputRequired()],
                                    render_kw={"placeholder":
                                               "Enter email address or username"})
    password = PasswordField("Password",
                             render_kw={"placeholder": "Enter password",
                                        "required": ""})
    submit = SubmitField("Log in")


class Search_and_filter_form(FlaskForm):
    search = StringField("Search",
                         render_kw={"placeholder": "Enter search term"})
    search_submit = SubmitField("Search")
    recipe_type = RadioField('Type', choices=[('All', 'All'),
                                              ('Meat', 'Meat'),
                                              ('Vegetarian', 'Vegetarian'),
                                              ('Vegan', 'Vegan')],
                                              default='All')
    cheap_checkbox = BooleanField('Cheap', render_kw={"value":
                                                      "Cheap"})
    gluton_free_checkbox = BooleanField('Gluten Free',
                                        render_kw={"value": "Gluton Free"})
    healthy_checkbox = BooleanField('Healthy', render_kw={"value":  "Healthy"})
    quick_checkbox = BooleanField('Quick', render_kw={"value": "Quick"})
    fakeaway_checkbox = BooleanField('Fakeaway', render_kw={"value":
                                                            "Fakeaway"})
    filter_submit = SubmitField('Add Filters')


class Add_recipe_form(FieldsRequiredForm):
    recipe_name = StringField('Recipe Name',
                              validators=[Length(min=4, max=50),
                                          InputRequired()],
                              render_kw={"minlength": "4",
                                         "maxlength": "50"})
    recipe_type = RadioField('Type', choices=[('Meat', 'Meat'),
                             ('Vegetarian', 'Vegetarian'),
                             ('Vegan', 'Vegan')])
    # Value attributes set here to make it quicker to put these values directly
    # into the recipe pages
    cheap_checkbox = BooleanField('Cheap', render_kw={"value":
                                                      "Cheap"})
    gluton_free_checkbox = BooleanField('Gluten Free',
                                        render_kw={"value": "Gluton Free"})
    healthy_checkbox = BooleanField('Healthy', render_kw={"value":  "Healthy"})
    quick_checkbox = BooleanField('Quick', render_kw={"value": "Quick"})
    fakeaway_checkbox = BooleanField('Fakeaway', render_kw={"value":
                                                            "Fakeaway"})
    ingredient_1 = StringField("Ingredient 1", validators=[InputRequired(),
                                                           Length
                                                           (min=3, max=50)],
                               render_kw={"minlength": "3", "maxlength": "50"})
    ingredient_2 = StringField("Ingredient 2", validators=[InputRequired()])
    ingredient_3 = StringField("Ingredient 3", validators=[InputRequired()])
    ingredient_optional = StringField()
    instruction_1 = TextAreaField("Instruction",
                                  validators=[InputRequired()],
                                  render_kw={"placeholder":
                                             "Please enter step 1..."})
    instruction_2 = TextAreaField("Instruction",
                                  validators=[InputRequired()],
                                  render_kw={"placeholder":
                                             "Please enter step 2..."})
    instruction_optional = TextAreaField("")
    feeds = IntegerField("How many people does it feed?",
                         validators=[InputRequired()],
                         render_kw={"type": "number", "min": "1"})
    picture_upload = FileField('Upload Picture',
                               render_kw={"accept": "image/*"},
                               validators=[FileAllowed(
                                       ['jpg', 'jpeg', 'png'],
                                       'Please add images only!')])
    new_picture_upload = FileField('New Picture Upload',
                                   render_kw={"accept": "image/*"},
                                   validators=[FileAllowed(
                                       ['jpg', 'jpeg', 'png'],
                                       'Please add images only!')])
    add_recipe_button = SubmitField(render_kw={"value": "Add Recipe"})
    edit_recipe_button = SubmitField(render_kw={"value": "Edit Recipe"})

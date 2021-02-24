from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField,
                     SubmitField, RadioField, BooleanField, TextAreaField)
from wtforms.validators import InputRequired, Length, Email, EqualTo
from wtforms.fields.html5 import EmailField


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
    email_or_username = StringField(
            "Email Address",
            render_kw={
             "placeholder": "Enter email address or username"})
    password = PasswordField("Password",
                             render_kw={"placeholder": "Enter password"})
    submit = SubmitField("Log in")


class Search_and_filter_form(FlaskForm):
    search = StringField("Search",
                         render_kw={"placeholder": "Enter search terms"})
    search_submit = SubmitField("Search")
    recipe_type = RadioField('Type', choices=[('meat', 'Meat'),
                                              ('vegetarian', 'Vegetarian'),
                                              ('vegan', 'Vegan')])
    cheap_checkbox = BooleanField('Cheap')
    gluton_free_checkbox = BooleanField('Gluton Free')
    healthy_checkbox = BooleanField('Healthy')
    quick_checkbox = BooleanField('Quick')
    fakeaway_checkbox = BooleanField('Fakeaway')
    filter_submit = SubmitField('Filter')


class Add_recipe_form(FlaskForm):
    recipe_type = RadioField('Type', choices=[('meat', 'Meat'),
                             ('vegetarian', 'Vegetarian'),
                             ('vegan', 'Vegan')])
    cheap_checkbox = BooleanField('Cheap')
    gluton_free_checkbox = BooleanField('Gluton Free')
    healthy_checkbox = BooleanField('Healthy')
    quick_checkbox = BooleanField('Quick')
    fakeaway_checkbox = BooleanField('Fakeaway')
    ingredient_1 = StringField("Ingredient 1",
                               validators=[Length(max=50), InputRequired()])
    ingredient_2 = StringField("Ingredient 2",
                                         validators=[Length(max=50)])
    quantity_1 = StringField("Quantity",
                             validators=[Length(max=50), InputRequired()])
    quantity_2 = StringField("Quantity",
                             validators=[Length(max=50),
                                         InputRequired()])
    instruction = TextAreaField("Instruction",
                                validators=[InputRequired()])
    additional_instructions = StringField("Instructions",
                                          validators=[Length(max=150)])

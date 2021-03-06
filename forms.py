from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField,
                     SubmitField, RadioField, BooleanField, TextAreaField,
                     IntegerField, FileField)
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
    cheap_checkbox = BooleanField('Cheap', render_kw={"required": False})
    gluton_free_checkbox = BooleanField('Gluton Free')
    healthy_checkbox = BooleanField('Healthy')
    quick_checkbox = BooleanField('Quick')
    fakeaway_checkbox = BooleanField('Fakeaway')
    filter_submit = SubmitField('Filter')


class Add_recipe_form(FieldsRequiredForm):
    recipe_name = StringField('Recipe Name',
                              validators=[Length(max=50), InputRequired()])
    recipe_type = RadioField('Type', choices=[('Meat', 'Meat'),
                             ('Vegetarian', 'Vegetarian'),
                             ('Vegan', 'Vegan')])
    cheap_checkbox = BooleanField('Cheap', render_kw={"value":
                                                      "Cheap"})
    gluton_free_checkbox = BooleanField('Gluton Free',
                                        render_kw={"value": "Gluton Free"})
    healthy_checkbox = BooleanField('Healthy', render_kw={"value":  "Healthy"})
    quick_checkbox = BooleanField('Quick', render_kw={"value": "Quick"})
    fakeaway_checkbox = BooleanField('Fakeaway', render_kw={"value":
                                                            "Fakeaway"})
    ingredient_1 = StringField("Ingredient 1", validators=[InputRequired()])
    ingredient_2 = StringField("Ingredient 2", validators=[InputRequired()])
    ingredient_3 = StringField("Ingredient 3", validators=[InputRequired()])
    instruction_1 = TextAreaField("Instruction",
                                  validators=[InputRequired()],
                                  render_kw={"placeholder":
                                             "Please enter step 1..."})
    instruction_2 = TextAreaField("Instruction",
                                  validators=[InputRequired()],
                                  render_kw={"placeholder":
                                             "Please enter step 2..."})
    feeds = IntegerField("How many people does it feed?",
                         validators=[InputRequired()],
                         render_kw={"type": "number"})
    picture_upload = FileField('Upload Picture')
    add_recipe_button = SubmitField(render_kw={"value": "Add Recipe"})


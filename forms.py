from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from wtforms.fields.html5 import EmailField


class Registration_form(FlaskForm):
    email = EmailField("Email Address",
                       validators=[Email(),
                                   InputRequired()])
    username = StringField("Username",
                           validators=[InputRequired(), Length(min=4, max=25)])
    password = PasswordField("Password",
                             validators=[InputRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm Password", validators=[
                                     InputRequired(), EqualTo('password')])
    submit = SubmitField("Register!")

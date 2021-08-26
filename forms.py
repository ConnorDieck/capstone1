from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, FloatField, PasswordField
from wtforms.validators import Email, InputRequired
from wtforms.fields.html5 import EmailField

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired(), Email()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class NotesForm(FlaskForm):
    text = StringField("Note Text", validators=[InputRequired()])
    discussion_date = StringField("Discussion Date", validators=[InputRequired()])

class DeleteForm(FlaskForm):
    """Form used to send POST requests in delete pathways"""
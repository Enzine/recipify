from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
  
class LoginForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=3)])
    password = PasswordField("Password", [validators.Length(min=8)])
    password_again = PasswordField("Password again", [validators.Length(min=8)])
  
    class Meta:
        csrf = False
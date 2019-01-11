# coding=utf-8
from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
import os

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipes.db"

# Print sql queries
app.config["SQLALCHEMY_ECHO"] = True

# Check which database to use.
if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipes.db"    
    app.config["SQLALCHEMY_ECHO"] = True

# Create db object
db = SQLAlchemy(app)

# Checks if user is authorized
from functools import wraps

def role_required(role="USER"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user:
                return login_manager.unauthorized()
          
            if not current_user.is_authenticated():
                return login_manager.unauthorized()
            
            if role == "ADMIN" and current_user.role != "ADMIN":
                return login_manager.unauthorized()
            
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

from app import views
from app.recipes import models, views
from app.auth import models, views
from app.comments import models, views

# Login
from app.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Create db tables
db.create_all()
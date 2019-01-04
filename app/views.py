from flask import render_template
from app import app
from app.recipes.models import Recipe

@app.route("/")
def index():
    return render_template("index.html", most_liked_recipes=Recipe.find_recipes_with_most_likes())
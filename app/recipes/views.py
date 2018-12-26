from app import app, db
from flask import render_template, request, url_for, redirect
from app.recipes.models import Recipe

@app.route("/recipes", methods=["GET"])
def recipes_index():
    return render_template("recipes/list.html", recipes = Recipe.query.all())

@app.route("/recipes/new/")
def recipes_form():
    return render_template("recipes/new.html")

@app.route("/recipes/<recipe_id>/", methods=["POST"])
def recipes_set_done(recipe_id):

    r = Recipe.query.get(recipe_id)
    r.done = True
    db.session().commit()
  
    return redirect(url_for("recipes_index"))

@app.route("/recipes/", methods=["POST"])
def recipes_create():
    r = Recipe(request.form.get("name"))

    db.session().add(r)
    db.session().commit()

    return redirect(url_for("recipes_index"))
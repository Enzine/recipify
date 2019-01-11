from app import app, db, role_required
from flask import render_template, request, url_for, redirect
from flask_login import current_user
from app.recipes.models import Recipe
from app.recipes.forms import RecipeForm
from app.comments.forms import CommentForm
import sys

# print('This is error output', file=sys.stderr)

# GET /recipes
# Shows list of recipes.
@app.route("/recipes", methods=["GET"])
def recipes_index():
    return render_template("recipes/list.html", recipes = Recipe.query.all())

# GET /recipes/<recipe_id>/show
# Shows one chosen recipe and its information.
@app.route("/recipes/<recipe_id>/show", methods=["GET"])
def recipes_show(recipe_id):
    return render_template("recipes/show.html", recipe = Recipe.query.get(recipe_id), form = CommentForm())

# GET /recipes/new
# Shows form to create a new recipe.
@app.route("/recipes/new/")
@role_required(role="USER")
def recipes_form():
    return render_template("recipes/new.html", form = RecipeForm())

# GET /recipes/<recipe_id>/edit
# Shows form to edit a chosen recipe.
@app.route("/recipes/<recipe_id>/edit/")
@role_required(role="USER")
def recipes_edit_form(recipe_id):
    return render_template("recipes/edit.html", recipe = Recipe.query.get(recipe_id), form = RecipeForm(obj=Recipe.query.get(recipe_id)))

# PUT /recipes/<recipe_id>/like
# Edits the given recipy by adding a like.
@app.route("/recipes/<recipe_id>/like/", methods=["POST"])
@role_required(role="USER")
def recipes_add_like(recipe_id):

    r = Recipe.query.get(recipe_id)
    r.likes += 1
    db.session().commit()
  
    return redirect(url_for("recipes_index"))

# POST /recipes
# Creates a new recipe.
@app.route("/recipes/", methods=["POST"])
@role_required(role="USER")
def recipes_create():
    form = RecipeForm(request.form)

    if not form.validate():
        return render_template("recipes/new.html", form = form)

    name = form.name.data
    preparation_time = form.preparation_time.data
    instructions = form.instructions.data
    account_id = current_user.id

    r = Recipe(name, preparation_time, instructions)
    r.account_id = current_user.id

    db.session().add(r)
    db.session().commit()

    return redirect(url_for("recipes_index"))

# PUT /recipes/<recipe_id>/edit
# Edits the given recipe.
@app.route("/recipes/<recipe_id>/edit/", methods=["POST"])
@role_required(role="USER")
def recipes_edit(recipe_id):
    form = RecipeForm(request.form)

    if not form.validate():
        return render_template("recipes/edit.html", recipe = Recipe.query.get(recipe_id), form = form)
    
    name = form.name.data
    preparation_time = form.preparation_time.data
    instructions = form.instructions.data
    
    r = Recipe.query.get(recipe_id)
    r.name = name
    r.preparation_time = preparation_time
    r.instructions = instructions

    db.session().commit()

    return redirect(url_for("recipes_index"))

# DELETE /recipes/<recipe_id>/delete
# Deletes a chosen recipe entity from database.
@app.route("/recipes/<recipe_id>/delete/", methods=["POST"])
@role_required(role="USER")
def recipes_remove(recipe_id):
    r = Recipe.query.get(recipe_id)
    
    db.session().delete(r)
    db.session().commit()

    return redirect(url_for("recipes_index"))

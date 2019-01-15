from app import app, db, role_required
from flask import render_template, request, url_for, redirect
from flask_login import current_user
from app.lykes.models import Lyke
from app.recipes.models import Recipe
from app.recipes.forms import RecipeForm
from app.comments.forms import CommentForm

@app.route("/recipes", methods=["GET"])
def recipes_index():
    return render_template("recipes/list.html", recipes = list(Recipe.query.order_by(Recipe.like_count.desc())))

@app.route("/recipes/<recipe_id>/show", methods=["GET"])
def recipes_show(recipe_id):
    return render_template("recipes/show.html", recipe = Recipe.query.get(recipe_id), form = CommentForm())

@app.route("/recipes/new/")
@role_required(role="USER")
def recipes_form():
    return render_template("recipes/new.html", form = RecipeForm())

@app.route("/recipes/<recipe_id>/edit/")
@role_required(role="USER")
def recipes_edit_form(recipe_id):
    return render_template("recipes/edit.html", recipe = Recipe.query.get(recipe_id), form = RecipeForm(obj=Recipe.query.get(recipe_id)))

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

@app.route("/recipes/<recipe_id>/delete/", methods=["POST"])
@role_required(role="USER")
def recipes_remove(recipe_id):
    r = Recipe.query.get(recipe_id)
    
    db.session().delete(r)
    db.session().commit()

    return redirect(url_for("recipes_index"))

@app.route("/recipes/<recipe_id>/like/", methods=["POST"])
@role_required(role="USER")
def recipes_add_like(recipe_id):
    r = Recipe.query.get(recipe_id)
    
    if current_user.id != r.account_id:
        query = Lyke.query.filter(Lyke.recipe_id == recipe_id).\
                filter(Lyke.account_id == current_user.id)
        
        liked = [value for value in query]

        if not liked:
            l = Lyke(recipe_id = recipe_id, account_id = current_user.id)
            
            r.like_count += 1
            db.session().add(l)
            db.session().commit()
  
    return redirect(url_for("recipes_index"))

import random

@app.route("/recipes/random/", methods=["GET"])
def recipes_random():
    recipes = Recipe.query.all()
    if not recipes:
        return redirect(url_for("index"))

    total = len(recipes)
    i = random.randint(0,total-1)

    r = recipes[i]

    return render_template("recipes/show.html", recipe = r, form = CommentForm())


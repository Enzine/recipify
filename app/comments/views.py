from app import app, db
from flask import render_template, request, url_for, redirect
from flask_login import login_required, current_user
from app.comments.models import Comment
from app.comments.forms import CommentForm
import sys

# print('This is error output', file=sys.stderr)

@app.route("/comments/<recipe_id>", methods=["POST"])
@login_required
def comments_create(recipe_id):
    form = CommentForm(request.form)

    if not form.validate():
        return redirect(url_for("recipes_show", recipe_id=recipe_id, form=form))

    c = Comment(form.text.data)
    c.account_id = current_user.id
    c.recipe_id = recipe_id

    db.session().add(c)
    db.session().commit()

    return redirect(url_for("recipes_show", recipe_id = recipe_id))

@app.route("/comments/<comment_id>/delete/", methods=["POST"])
@login_required
def comments_remove(comment_id):
    c = Comment.query.get(comment_id)
    
    db.session().delete(c)
    db.session().commit()

    return redirect(url_for("recipes_show", recipe_id = c.recipe_id))
# coding=utf-8
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from app import app, db
from app.auth.models import User
from app.auth.forms import LoginForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/login.html", form = LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/login.html", form = form,
                               error = "No such username or password")

    login_user(user)
    return redirect(url_for("index"))

@app.route("/auth/register", methods = ["GET", "POST"])
def auth_register():
    if request.method == "GET":
        return render_template("auth/register.html", form = LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        user = User(form.username.data, form.password.data)

        db.session().add(user)
        db.session().commit()

        login_user(user)
    else: 
        return render_template("auth/register.html", form = form,
                               error = "Username is already taken.")
    
    return redirect(url_for("index"))   

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))    

@app.route("/auth/<account_id>/show", methods=["GET"])
def auth_show(account_id):
    return render_template("auth/show.html", account = User.query.get(account_id))
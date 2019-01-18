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

    user = User.query.filter_by(username=form.username.data).first()
    if not user:
        return render_template("auth/login.html", form = form,
                            error = "No such username")

    if user.is_correct_password(form.password.data):
        login_user(user)

        return redirect(url_for("index"))
    else:
        return render_template("auth/login.html", form = form,
                            error = "Given password doesn't match this user")

@app.route("/auth/register", methods = ["GET", "POST"])
def auth_register():
    if request.method == "GET":
        return render_template("auth/register.html", form = LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data).first()

    if not user:
        if form.password.data != form.password_again.data:
            return render_template("auth/register.html", form = form,
                            error = "Password fields need to match.")
                               
        if not form.validate_on_submit():
            return render_template("auth/register.html", form = LoginForm(),
                            error = "Username must be at least 3 characters. Password at least 8 characters long.")
        
        user = User(form.username.data)
        user.password = form.password.data

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
# coding=utf-8
from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
# Kolme vinoviivaa kertoo, tiedosto sijaitsee tämän sovelluksen 
# tiedostojen kanssa samassa paikassa
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipes.db"

# Pyydetään SQLAlchemyä tulostamaan kaikki SQL-kyselyt
app.config["SQLALCHEMY_ECHO"] = True

# Luodaan db-olio, jota käytetään tietokannan käsittelyyn
db = SQLAlchemy(app)

from app import views

from app.recipes import models, views
# Luodaan lopulta tarvittavat tietokantataulut
db.create_all()
from app import db
from app.models import Base
from sqlalchemy.sql import text

class Recipe(Base):

    name = db.Column(db.String(144), nullable=False)
    preparation_time = db.Column(db.Integer)
    instructions = db.Column(db.String, nullable=False)
    like_count = db.Column(db.Integer)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    comments = db.relationship('Comment', backref='recipe', lazy=True)
    likes = db.relationship('Lyke', backref='recipe', lazy=True)

    def __init__(self, name, preparation_time, instructions):
        self.name = name
        self.preparation_time = preparation_time
        self.instructions = instructions
        self.like_count = 0

    @staticmethod
    def find_recipes_with_most_likes():

        stmt = text("SELECT Recipe.id, Recipe.name, COUNT(Lyke.id), Lyke.recipe_id FROM Recipe JOIN Lyke ON Recipe.id = Lyke.recipe_id GROUP BY Recipe.id, Lyke.recipe_id ORDER BY COUNT(Lyke.id) DESC;")

        res = db.engine.execute(stmt)

        response = [{"id":row[0], "name":row[1], "likes":row[2]} for row in res]

        return response[:5]
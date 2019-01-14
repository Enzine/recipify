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
    likes = db.relationship('Like', backref='recipe', lazy=True)

    def __init__(self, name, preparation_time, instructions):
        self.name = name
        self.preparation_time = preparation_time
        self.instructions = instructions
        self.like_count = 0

    @staticmethod
    def find_recipes_with_most_likes():

        stmt = text("SELECT Recipe.id, Recipe.name, Count(Like.id), Like.recipe_id FROM Recipe"
                    " JOIN Like ON Recipe.id = Like.recipe_id"
                    " GROUP BY Recipe.id"
                    " ORDER BY COUNT(Like.id)" 
                    " DESC;")

        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1], "likes":row[2]})

        return response[:5]
from app import db
from app.models import Base
from sqlalchemy.sql import text

class Recipe(Base):

    name = db.Column(db.String(144), nullable=False)
    done = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    preparation_time = db.Column(db.Integer)
    instructions = db.Column(db.String, nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    comments = db.relationship('Comment', backref='recipe', lazy=True)

    def __init__(self, name, preparation_time, instructions):
        self.name = name
        self.done = 0
        self.likes = 0
        self.preparation_time = preparation_time
        self.instructions = instructions

    @staticmethod
    def find_recipes_with_most_likes():

        stmt = text("select recipe.id, recipe.name, recipe.likes from recipe where recipe.likes > 0 order by recipe.likes desc;")

        # stmt = text("SELECT Recipe.id, Recipe.name, Recipe.likes FROM Recipe"
        #              " WHERE Recipe.likes > 0"
        #              " ORDER BY Recipe.likes"
        #              " DESC;")

        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1], "likes":row[2]})

        return response[:5]
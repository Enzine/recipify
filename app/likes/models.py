from app import db
from app.models import Base

class Like(Base):

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __init__(self, recipe_id, account_id):
        self.recipe_id = recipe_id
        self.account_id = account_id
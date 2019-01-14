from app import db
from app.models import Base

class User(Base):

    __tablename__ = "account"

    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)
    role = db.Column(db.String(80), nullable=False)

    likes = db.relationship("Like", backref='like', lazy=True)
    recipes = db.relationship("Recipe", backref='account', lazy=True)
    comments = db.relationship('Comment', backref='account', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.role = "USER"
  
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
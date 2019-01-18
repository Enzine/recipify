from app import db, bcrypt
from app.models import Base

from sqlalchemy.ext.hybrid import hybrid_property

class User(Base):

    __tablename__ = "account"

    username = db.Column(db.String(64), unique=True, nullable=False)
    _password = db.Column(db.String(128))
    
    role = db.Column(db.String(80), nullable=False)

    likes = db.relationship("Lyke", backref='account', lazy=True)
    recipes = db.relationship("Recipe", backref='account', lazy=True)
    comments = db.relationship('Comment', backref='account', lazy=True)

    def __init__(self, username):
        self.username = username
        self.role = "USER"
  
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)
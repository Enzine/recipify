from app import db

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())

    name = db.Column(db.String(144), nullable=False)
    done = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    preparation_time = db.Column(db.Integer)
    instructions = db.Column(db.String, nullable=False)

    def __init__(self, name, preparation_time, instructions):
        self.name = name
        self.done = 0
        self.likes = 0
        self.preparation_time = preparation_time
        self.instructions = instructions
 
    @classmethod
    def by_id(cls, id):
        return db.session().query(Recipe).filter(Recipe.id==id)
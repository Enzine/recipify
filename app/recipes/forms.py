from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, validators

class RecipeForm(FlaskForm):
    name = StringField("Recipe name", [validators.InputRequired()])
    preparation_time = IntegerField("Preparation time (mins)", [validators.Optional()])
    instructions = TextAreaField("Instructions", [validators.InputRequired()], render_kw={"rows": 12, "cols": 45})
 
    class Meta:
        csrf = False
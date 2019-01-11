from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, validators

class CommentForm(FlaskForm):
    text = TextAreaField("Your comment", [validators.InputRequired()], render_kw={"rows": 6, "cols": 45})

    class Meta:
        csrf = False
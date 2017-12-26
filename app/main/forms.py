from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField, SubmitField
from wtforms.validators import Required, DataRequired


class ContentForm(FlaskForm):
    id = IntegerField('id')
    name = StringField('name', validators=[DataRequired()])
    text = TextAreaField('text')
    submit = SubmitField('Submit')
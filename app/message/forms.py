from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, HiddenField, TextAreaField
from wtforms.validators import Required, ValidationError, DataRequired

from app.models import UserModel


class SendForm(FlaskForm):
    user_id = HiddenField('user_id', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')

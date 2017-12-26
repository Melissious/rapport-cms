from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField
from wtforms.validators import Required, ValidationError, DataRequired, Length, EqualTo, Email, NumberRange, Regexp

from app.models import UserModel


class LoginForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired(), Length(min=3, max=30), Regexp('^\w+$', message="Username must contain only letters numbers or underscore")])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=4, max=50)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=4, max=30), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Repeat pass', validators=[DataRequired()])
    sex = SelectField('Sex', validators=[DataRequired(), NumberRange(min='1', max='2')],
                      choices=[("1", "Male"), ("2", "Female")])
    submit = SubmitField('Reg It!')

    def validate_email(self, field):
        if UserModel.query.filter_by(email=field.data).first():
            raise ValidationError('Email already exists')

    def validate_username(self, field):
        if UserModel.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists')

    def validate_password(self, field):
        if field.data==self.username.data:
            raise ValidationError('Password and username must be unsame')
        if field.data==self.email.data:
            raise ValidationError('Password and email must be unsame')
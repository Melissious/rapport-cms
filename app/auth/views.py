from flask import render_template, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import redirect

from app import db
from app.models import UserModel
from .forms import LoginForm, RegistrationForm
from . import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Wrong login ot password')
    return render_template('auth/login.html', form=form)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Success log in')
    return redirect(url_for('main.index'))


@auth.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        logout_user()
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = UserModel(email=form.email.data,
                             username=form.username.data,
                             password=form.password.data,
                             sex=form.sex.data)
            db.session.add(user)
            db.session.flush()
            flash('Registration success')
            login_user(user)
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash(e.args[0])
    return render_template('auth/registration.html', form=form)

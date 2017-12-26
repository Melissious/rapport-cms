from datetime import datetime
from flask import render_template, request, redirect, flash, url_for
from flask_login import login_required

from ..models import ContentModel, UserModel
from .forms import ContentForm
from . import main
from .. import db


@main.route('/')
def index():
    contents = ContentModel.query.all()
    user_agent = request.headers.get('User-Agent')
    return render_template('index.html', user_agent=user_agent, contents=contents, current_time=datetime.utcnow())


@main.route('/content/<int:id>')
def content(id):
    content = ContentModel.query.filter_by(id=id).first_or_404()
    return render_template('content.html', content=content)


@main.route('/content/new', methods=['GET', 'POST'])
@login_required
def content_new():
    form = ContentForm()
    if form.validate_on_submit():
        content_model = ContentModel(name=form.name.data, text=form.text.data)
        db.session.add(content_model)
        db.session.commit()
        flash('Success added content')
        return redirect(url_for('main.index'))

    return render_template('content_new.html', form=form)


@main.route('/user/<name>')
def user(name):
    user = UserModel.query.filter_by(username=name).first_or_404()
    return render_template('user.html', user=user)

@main.route('/users')
def users():
    users = UserModel.query.all()
    return render_template('users.html', users=users)


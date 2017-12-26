from app import db
from app.message.forms import SendForm
from app.models import UserModel, MessageModel
from . import message
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

# All yourself messages
@message.route('/', methods=['GET'])
@login_required
def messages():
    list = MessageModel.query.filter_by(user_id=current_user.user_id)
    return render_template('messages/all.html', messages=list)

# New youself messages
@message.route('/new', methods=['GET'])
@login_required
def new_messages():
    list = MessageModel.query.filter_by(user_id=current_user.user_id, read=0)
    return render_template('messages/new_messages.html', messages=list)

# Messages with other user
@message.route('/<int:user_id>', methods=['GET'])
@login_required
def dialog(user_id):
    other_user = UserModel.query.filter_by(user_id=user_id).first_or_404()
    list = MessageModel.query.filter_by(user_id=current_user.user_id, other_user_id=other_user.user_id)
    return render_template('messages/dialog.html', messages=list, other_user=other_user)

# Send message
@message.route('/send/<int:user_id>', methods=['GET', 'POST'])
@login_required
def send_message(user_id):
    if user_id == current_user.user_id:
        flash('Invalid user')
        return redirect(redirect_url())
    other_user = UserModel.query.filter_by(user_id=user_id).first_or_404()
    form = SendForm()
    form.user_id.data = user_id
    if form.validate_on_submit():
        try:
            MessageModel.send_message(current_user.user_id, user_id, form.message.data)
            db.session.flush()
            flash('Success sended')
            return redirect(url_for('message.dialog', user_id=user_id))
        except Exception as e:
            db.session.rollback()
            flash(e.args[0])
    return render_template('messages/send.html', other_user=other_user, form=form)

# Read message
@message.route('/read/<int:message_id>', methods=['GET'])
@login_required
def message_read(message_id):
    message = MessageModel.query.filter_by(message_id=message_id, user_id=current_user.user_id).first_or_404()
    message.readed()
    return render_template('messages/read.html', message=message)

# Mark all as readed
@message.route('/readall', methods=['GET'])
@login_required
def read_all():
    MessageModel.readed_all(current_user.user_id)
    return redirect(redirect_url())


# Delete message
@message.route('/del/<int:message_id>', methods=['GET'])
@login_required
def message_del(message_id):
    message = MessageModel.query.filter_by(message_id=message_id, user_id=current_user.user_id).first_or_404()
    db.session.delete(message)
    db.session.commit()
    flash('Success message deleted')
    return redirect(url_for('message.messages'))

def redirect_url(default='message.messages'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)

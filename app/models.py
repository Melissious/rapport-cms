import datetime
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app.const import Const
from . import db, login_manager


class ContentModel(db.Model):
    __tablename__ = 'content'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    text = db.Column(db.Text(4000))

    def __repr__(self):
        return '<Content %s>' % self.id


class UserModel(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True)
    email = db.Column(db.String(50), index=True)
    password_hash = db.Column(db.String(128))
    sex = db.Column(db.Integer)

    # messages = relationship("MessageModel",
    #                         backref='user_message_list')

    @property
    def password(self):
        raise AttributeError('password not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.user_id)

class MessageModel(db.Model):
    __tablename__ = 'message'
    message_id = db.Column(db.Integer, primary_key=True)
    direct = db.Column(db.Integer)
    user_id = db.Column(db.Integer, ForeignKey('user.user_id'))
    other_user_id = db.Column(db.Integer, ForeignKey('user.user_id'))
    message = db.Column(db.String(500))
    read = db.Column(db.Integer, default=Const.UNREAD)
    send_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    user = relationship("UserModel", uselist=False, backref='user_first', foreign_keys=[user_id])
    other_user = relationship("UserModel", uselist=False, backref='user_second', foreign_keys=[other_user_id])

    def readed(self):
        self.read = Const.READED
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def readed_all(user_id):
        sql = "UPDATE `message` SET `read` = :new_status WHERE `user_id`=:user_id AND `read` = :old_status"
        db.session.execute(sql, {'new_status': Const.READED, 'user_id':user_id, 'old_status':Const.UNREAD})
        db.session.commit()

    @staticmethod
    def send_message(from_user, to_user, message):
        mes1 = MessageModel()
        mes1.user_id = from_user
        mes1.other_user_id = to_user
        mes1.direct = Const.OUT
        mes1.message = message
        mes1.read = Const.READED
        db.session.add(mes1)
        mes2 = MessageModel()
        mes2.user_id = to_user
        mes2.other_user_id = from_user
        mes2.direct = Const.IN
        mes2.message = message
        mes2.read = Const.UNREAD
        db.session.add(mes2)
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))

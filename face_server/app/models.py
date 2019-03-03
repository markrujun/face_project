import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, current_app
from flask_login import UserMixin
from app import db, login_manager
from config import config
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(64), primary_key=True)
    password_hash = db.Column(db.String(128))
    photoName = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(64), nullable=True)
    department = db.Column(db.String(128), nullable=True)
    sex = db.Column(db.String(8), nullable=True)
    lastStatus = db.Column(db.Integer,default=1) # 1是未上传， 2是等待审核， 3是正在审核， 4是审核未通过， 5是审核通过


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {self.username}>'.format(self=self)

    def generate_auth_token(self, expiration=6000):
        s = Serializer(current_app.config["SECRET_KEY"],
                        expires_in=expiration)
        return s.dumps({'username': self.username})
    

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(64), nullable=False)
    uploadPhotoName = db.Column(db.String(255), nullable=False)
    confidence = db.Column(db.Float)
    time = db.Column(db.DateTime, default=datetime.datetime.now)
    status = db.Column(db.Integer, primary_key=True)
    adminname =  db.Column(db.String(64) ,nullable=True)
    mark = db.Column(db.String(225), nullable=True)


class Admin(db.Model):
    __tablename__ = 'admin'
    adminname =  db.Column(db.String(64),primary_key=True)
    password_hash = db.Column(db.String(128),nullable=False)
    permission = db.Column(db.Integer, default=1, nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=6000):
        print(current_app.config)
        s = Serializer(current_app.config.get("SECRET_KEY"),
                        expires_in=expiration)
        return s.dumps({'adminname': self.adminname})
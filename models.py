from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin, current_user
from time import time
import jwt
from app import app, login
from flask import session


followers = db.Table(
    'followers',
    db.Column('participant_id', db.Integer, db.ForeignKey('participant.id'), primary_key=True),
    db.Column('entrepeneur_id', db.Integer, db.ForeignKey('entrepeneur.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    __abstract__ = True
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    __sal = "Sal De Prueba"


    def set_password(self, password):
        self.password_hash = generate_password_hash(password + self.__sal)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password + self.__sal)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password':self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


    def __repr__(self):
        return f'<User {self.username}>'


class Participant(User):
    __tablename__ = "Participant"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    income = db.Column(db.String(128))
    position = db.Column(db.String(128))
    education = db.Column(db.String(128))
    # country = db.Column(db.String(128))
    survey_history = db.Column(db.String(128))


    def __repr__(self):
        return f'<Participant {self.username}>'


class Entrepeneur(User):
    __tablename__ = "Entrepeneur"
    id = db.Column(db.Integer, primary_key=True)
    surveys = db.Column(db.String(128))
    company = db.Column(db.String(128), unique=True)
    # logo = db.Column(db.BLOB)
    # followers = db.relationship(
    #     'participant', secondary=followers, lazy=subquery,
    #     backref=db.backref('followed_company', lazy='subquery')

    def __repr__(self):
        return f'<Entrepeneur {self.username}>'


class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    #id_entrepeneur = (db.Integer)
    questions = db.relationship('Question', backref='survey', lazy='dynamic')
    reward = db.Column(db.Integer)
    develop_cost = db.Column(db.Integer)

    def __repr__(self):
        return f'<Survey {self.id}>'

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(256))
    answer = db.Column(db.String(256))
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'))
    #id_participant = db.Column(db.Integer)

    def __repr__(self):
        return f'<Question {self.id}>'

@login.user_loader
def load_user(user_id):
    # if session_part == 'Participant':
    if session.get('account_type') == 'Participant':
        return Participant.query.get(int(user_id))
    else:
        return Entrepeneur.query.get(int(user_id))

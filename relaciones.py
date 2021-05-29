from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Prize(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String(128))
    qbuckz = db.Column(db.Integer)
    service = db.Column(db.String(128))

###################################################################

association = db.Table('followers',
                       db.Column('follower_participant_id', db.Integer, db.ForeignKey('Participant.id')),
                       db.Column('followed_entrepeneur_id', db.Integer, db.ForeignKey('Entrepeneur.id'))
                       )

class User(db.Model):
    __abstract__ = True
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    __sal = "Sal De Prueba"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password + self.__sal)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password + self.__sal)

    def __repr__(self):
        return f'<User {self.username}>'


class Participant(UserMixin, User):
    __tablename__ = "Participant"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    income = db.Column(db.String(128))
    position = db.Column(db.String(128))
    education = db.Column(db.String(128))
    # country = db.Column(db.String(128))
    survey_history = db.Column(db.String(128))

    followed = db.relationship(
        'Entrepeneur',
        secondary=association,
        primaryjoin=(association.c.follower_participant_id == id),
        secondaryjoin=(association.c.followed_entrepeneur_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(association.c.followed_entrepeneur_id == user.id).count() > 0

    def __repr__(self):
        return f'<Participant {self.name}>'


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
        return f'<Entrepeneur {self.company}>'

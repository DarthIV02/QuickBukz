from app import db
from werkzeug.security import generate_password_hash, check_password_hash


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


class Participant(User):
    __tablename__ = "Participant"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    income = db.Column(db.Float)
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
    logo = db.Column(db.BLOB)

    def __repr__(self):
        return f'<Entrepeneur {self.username}>'



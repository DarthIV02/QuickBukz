from app import app, db
from flask import render_template, flash, redirect, url_for
from app.forms import RegisterForm, RegisterFormParticipant, RegisterFormEntrepeneur, LoginForm
from app.models import Entrepeneur, Participant

# app = Flask(__name__)
@app.route('/', methods=['GET'])
def home():
    return 'Home page'

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        global user
        user = {'email': form.email.data, 'password':form.password.data}
        if form.type_of_user.data == 'participant':
            return redirect(url_for('participant_registry'))
        return redirect(url_for('entrepeneur_registry'))

    return render_template('register.html', form=form)


@app.route('/participant_registry', methods=['GET', 'POST'])
def participant_registry():
    form = RegisterFormParticipant()
    if form.validate_on_submit():
        part = Participant(email=user['email'], password=['password'], name=form.name.data,
                           income=form.income.data, position=form.education.data,
                           education=form.education.data)
        db.session.add(part)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/entrepeneur_registry', methods=['GET', 'POST'])
def entrepeneur_registry():
    form = RegisterFormEntrepeneur()
    if form.validate_on_submit():
        ent = Entrepeneur(email=user['email'], password=user['password'], company=form.company.data)
        db.session.add(ent)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.email.data, form.remember_me.data))
        return redirect(url_for('home'))
    return render_template('login.html',  title='Sign In', form=form)

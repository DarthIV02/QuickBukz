from app import app, db, principals, enter_permission
from flask import render_template, flash, redirect, url_for, request, session, request
from app.forms import RegisterForm, RegisterFormParticipant, RegisterFormEntrepeneur,\
    LoginForm, CreateQuestion, ResetPasswordRequestForm, ResetPasswordForm, Add_RemoveQuestion, \
    Option, AddOption, Questions, NumberofQuestions
from app.models import Entrepeneur, Participant, User, Prize, Survey, Question
from flask_login import current_user, login_user, logout_user, login_required

from app.email import send_password_reset_email

    # app = Flask(__name__)
@app.route('/')
@app.route('/main_menu')
def main_menu():
    return render_template('main_menu.html', title='Main Menu')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        global user
        user = {'email': form.email.data, 'password': form.password.data}
        if form.type_of_user.data == 'participant':
            return redirect(url_for('participant_registry'))
        return redirect(url_for('entrepeneur_registry'))

    return render_template('register.html', title="Register" , form=form)


@app.route('/participant_registry', methods=['GET', 'POST'])
def participant_registry():
    form = RegisterFormParticipant()
    if form.validate_on_submit():
        global user
        part = Participant(email=user['email'], name=form.name.data,
                           income=form.income.data, position=form.education.data,
                           education=form.education.data)
        part.set_password(user['password'])
        db.session.add(part)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', title='Participant Registry', form=form)


@app.route('/entrepeneur_registry', methods=['GET', 'POST'])
def entrepeneur_registry():
    form = RegisterFormEntrepeneur()
    if form.validate_on_submit():
        global user
        ent = Entrepeneur(email=user['email'], company=form.company.data)
        ent.set_password(user['password'])
        db.session.add(ent)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', title='Entrepeneur Registry', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.email.data
        part_email = Participant.query.filter_by(email=username).first()
        ent_email = Entrepeneur.query.filter_by(email=username).first()
        user = Participant.query.filter_by(email=username).first() or Entrepeneur.query.filter_by(email=username).first()

        if (user is None):
            flash('Wrong email, are you registered?')
            return redirect(url_for('login'))
        elif not user.check_password(form.password.data):
            flash('Wrong password')
            return redirect(url_for('login'))
        else:
            if user == part_email:
                session['account_type'] = 'Participant'
                login_user(user, remember=form.remember_me.data)
                flash('Login requested for email {}, remember_me={}'.format(form.email.data, form.remember_me.data))
                return redirect(url_for('home'))
            if user == ent_email:
                session['account_type'] = 'Entrepeneur'
                login_user(user, remember=form.remember_me.data)
                flash('Login requested for email {}, remember_me={}'.format(form.email.data, form.remember_me.data))
                return redirect(url_for('entrepeneur_home'))

        # next_page=request.args.get('next')
        # if not next_page or url_parse(next_page).netloc != '':
        #     next_page = url_for('index')
        # return redirect(next_page)
    return render_template('login.html',  title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_menu'))

@app.route('/create_0')
def create_0():
    pass

@app.route('/create', methods=['GET', 'POST'])
def create():
    num_of_questions = request.args.get('num_of_questions')
    other_form=CreateQuestion()
    return render_template('create2.html', num=int(num_of_questions), form=other_form)


@app.route('/create2', methods=['GET', 'POST'])
def create2():
    form = NumberofQuestions()
    if form.validate_on_submit():
        return redirect(url_for('create', num_of_questions=form.numofquestions.data))
    return render_template('create.html', form=form)

@app.route('/save_questions', methods=['GET', 'POST'])
def save_questions():
    if request.method == 'POST':
        preguntas = request.form
        num = request.args.get('num')
        print(preguntas['question'])
        # s = Survey(id_entrepeneur=current_user.id, reward=5*num, develop_cost=10*num)
        # for i in range(num):
        #     q = Question(text=preguntas[0][1])

        return render_template('resultados.html', resultado=preguntas)

@app.route('/about_us', methods=['GET', 'POST'])
def about_us():
    return render_template('about_us.html', title='About Us',)

@app.route('/support', methods=['GET', 'POST'])
def support():
    return render_template('support.html', title='Support',)

@app.route('/password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            User.send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('password_request.html',
                           title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", title='Home Page', user=current_user)

@app.route('/entrepeneur_home', methods=['GET', 'POST'])
@login_required
def entrepeneur_home():
    return render_template("entrepeneur_home.html", title='E. Home Page', user=current_user)


# @app.route('/entrepeneur/<email>')
# @login_required
# def entrepeneur(email):
#     email = Entrepeneur.query.filter_by(email=email).first_or_404()
#     return render_template('entrepeneur_home.html', email=email)
#
# @app.route('/participant/<email>')
# @login_required
# def participant(email):
#     email = Participant.query.filter_by(email=email).first_or_404()
#     return render_template('home.html', email=email)

@app.route('/available_surveys')
def available_survey():
#     surveys = Survey.query.join(
# Participant, ((Participant.c.income == Survey.income_part) and (Survey.income_part != None))).filter(
# followers.c.follower_id == self.id).order_by(
# Post.timestamp.desc())
    surveys = current_user.surveys_available()
    return render_template('available_survey.html', surveys=surveys)

@app.route('/my_surveys')
def my_surveys():
    pass

@app.route('/my_stats')
def my_stats():
    return render_template('my_stats', title='stats')

@app.route('/view_prizes', methods=['GET','POST'])
def view_prizes():
    if request.method == 'GET':
        prizes = Prize.query.all()
        print(prizes)
        return render_template('view_prizes.html', prizes=prizes)


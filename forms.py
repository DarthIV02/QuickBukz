from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField, \
    DateField, SelectField, FileField, FieldList, FormField, Form, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from wtforms.fields.html5 import DateField
from app.models import User
import pycountry
from app import app
from app.models import User

class RegisterForm(FlaskForm):
    type_of_user = RadioField('Type of Users', choices=[('participant', 'Participant'), ('entrepeneur', 'Entrepeneur')],
                              validators=[DataRequired()])
        # 'valor para nosotros', 'lo que se despliega'
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Continue')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user is not None:
            raise ValidationError('Please use a different email address.')


class RegisterFormParticipant(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    gender = SelectField(label='Gender', choices=[('masculine','Masculine'), ('femenine','Femenine'), ('none','None'), ('other','Other')])
    date_of_birth = DateField('Date of Birth')
    #format="datetime.format(%d/%m/%y)"
    income = SelectField(label='Anual Income', choices=[('very low', "$0-$10,000"),('low', '$10,000 - $50,000'),
                                                 ("medium", '$50,000 - $150,000'), ("high", '$150,000+')])
    #country = SelectField('Country', options=[(country.lower(), country) for country in pycountry.countries])
    education = SelectField(label='Education',choices=[('high_school', 'High School'),('university', 'University'),
                                                 ('post_graduate','Post Graduate')])
    position = SelectField(label='Position', choices=[('student', 'Student'), ('unemployed', 'Unemployed'), ('employed', 'Employed'),
                                               ('freelancer', 'Freelancer'), ('retired', 'Retired')])
    submit = SubmitField('Register')


class RegisterFormEntrepeneur(FlaskForm):
    company = StringField(label='Company', validators=[DataRequired()])
    logo = FileField(label='Logo')
    submit = SubmitField('Register')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class CreateQuestion(Form):
    question = StringField(label='Insert a question', validators=[DataRequired()])

class NumberofQuestions(FlaskForm):
    numofquestions = IntegerField(label='Insert the number of questions', validators=[DataRequired()])
    # 

class Questions(FlaskForm):
    questions = FieldList(FormField(CreateQuestion), min_entries= 1)
    addq = SubmitField(label='Add another question')
    remq = SubmitField(label='Remove another question')
    submit = SubmitField(label='Submit')

class Add_RemoveQuestion(FlaskForm):
    addq = SubmitField(label='Add another question')
    remq = SubmitField(label='Remove another question')
    submit = SubmitField(label='Submit')


class AddOption(FlaskForm):
    addop = SubmitField(label='Add Another Option')

class Option(FlaskForm):
    option = StringField(label='Option')

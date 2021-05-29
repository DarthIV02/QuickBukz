from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField, \
    DateField, SelectField, FileField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from wtforms.fields.html5 import DateField
import pycountry

class RegisterForm(FlaskForm):
    type_of_user = RadioField(label='Type of Users', choices=[('participant', 'Participant'), ('entrepeneur', 'Entrepeneur')],
                              validators=[DataRequired()])
        # 'valor para nosotros', 'lo que se despliega'
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    password2 = PasswordField(label='Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Continue')


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

class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField(label='Remember Me')
    submit = SubmitField('Sign In')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import DateField
from todosapp.model import User, ToDo
from datetime import datetime

class RegistrationForm(FlaskForm):
    name = StringField('Name',
        validators=[DataRequired(), Length(min=2, max=20)])
    email= StringField('Email',
        validators=[DataRequired(), Email()])
    password= PasswordField('Password', validators=[DataRequired()])
    confirm_password= PasswordField('Confirm Password',
         validators=[DataRequired(), EqualTo('password')])
    submit= SubmitField('Sing Up')

    def validate_email(self ,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Duplicate Email')

class LoginForm(FlaskForm):
    email= StringField('Email',
        validators=[DataRequired(), Email()])
    password= PasswordField('Password', validators=[DataRequired()])
    remember= BooleanField('Remember Me')
    submit= SubmitField('Login')

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    priority = SelectField('Priority', choices=[(1, 'High'), (2, 'Medium'), (3, 'Low')])
    end_date= DateField('End Date', default=datetime.today, format='%Y-%m-%d', validators=[DataRequired()])
    current_date=datetime.today()
    submit = SubmitField('Task')

class ForgotPasswordForm(FlaskForm):
    email= StringField('Email',validators=[DataRequired(), Email()])
    password= PasswordField('Password', validators=[DataRequired()])
    confirm_password= PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit= SubmitField('New Password')

    def validate_email(self ,email):
        user=User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("Email not found")
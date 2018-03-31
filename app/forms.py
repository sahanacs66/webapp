from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired,Email

class RegisterForm(FlaskForm):
        username = StringField('Username',validators = [DataRequired()])
        firstName = StringField('FirstName',validators = [DataRequired()])
        lastName = StringField('LastName', validators = [DataRequired()])
        email = StringField('Email', validators = [DataRequired(),Email()])
        password = PasswordField('Password', validators=[DataRequired()])
        submit = SubmitField('Register')

class SearchForm(FlaskForm):
        search = StringField('search',validators=[DataRequired()])
        submit = SubmitField('find')

class LoginForm(FlaskForm):
        username = StringField('Username',validators = [DataRequired()])
        password = PasswordField('password', validators=[DataRequired()])
        submit = SubmitField('login')

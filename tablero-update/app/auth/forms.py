from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import Required, Email, Length, Regexp

class LoginForm(FlaskForm):
    email = StringField('Email', validators= [Required(message= 'Error Fill'),Email(message= 'Error Mail'), Length(message= 'Error L',min = 10, max = 64)])
    password = PasswordField('Password', validators= [Required()])
    remember_me = BooleanField('Remember')
    submit = SubmitField('Log In')
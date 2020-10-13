from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length


class SignInForm(FlaskForm):
    username = StringField('User name', validators=[DataRequired(), Length(min=4, max=32, message='Nombre usuario no valido')])
    password = PasswordField('Password',validators=[DataRequired(), Length(min=8, max=32, message='Contraseña no valida')])
    submit = SubmitField('Sign in')


class SignUpForm(FlaskForm):

    username=StringField('User Name', validators=[DataRequired(), Length(min=4, max=32, message='Nombre usuario no valido')])
    email=StringField('Email', validators=[DataRequired(), Length(min=4, max=32, message='Correo electrónico no valido')])
    name=StringField('Name', validators=[DataRequired(), Length(min=4, max=32, message='Nombre no valido')])
    password=PasswordField('Password', validators=[DataRequired(), Length(min=8, max=32, message='Password no valido')])
    #Mensaje de confirmación de password
    retry_password = PasswordField('Confirm your password', validators=[DataRequired(), Length(min=4, max=32, message='Confirmación no valida')])
    submit = SubmitField('Sign Up')




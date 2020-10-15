from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length


class SignInForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=4, max=32, message='Nombre usuario no valido')])
    password = PasswordField('Contraseña',validators=[DataRequired(), Length(min=8, max=32, message='Contraseña no valida')])
    submit = SubmitField('Iniciar Sesión')


class SignUpForm(FlaskForm):

    username=StringField('Nombre de usuario', validators=[DataRequired(), Length(min=4, max=32, message='Nombre usuario no valido')])
    email=StringField('Correo electronico', validators=[DataRequired(), Length(min=4, max=32, message='Correo electrónico no valido')])
    name=StringField('Nombre', validators=[DataRequired(), Length(min=4, max=32, message='Nombre no valido')])
    password=PasswordField('Contraseña', validators=[DataRequired(), Length(min=8, max=32, message='Contraseña no valido')])
    #Mensaje de confirmación de password
    retry_password = PasswordField('Confirma la contraseña', validators=[DataRequired(), Length(min=4, max=32, message='Confirmación no valida')])
    submit = SubmitField('Crear cuenta')




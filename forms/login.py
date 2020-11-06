from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, Email, AnyOf

# Formulario para el login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(message="Debe ingresar su email"), Email(message="El email ingresado no es válido")])
    password = PasswordField('Password', validators=[InputRequired(message="Debe ingresar su contraseña")])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')
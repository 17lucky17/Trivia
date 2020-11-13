from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegisterForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired(message="Dato requerido")])
    email = StringField('Email', validators=[DataRequired(message="Dato requerido"), Email(message="El email ingresado no es válidoo")])
    password = PasswordField('Contraseña', validators=[DataRequired(message="Dato requerido"),Length(min=5, max=12,message="El largo de la contraseña debe ser entre 5 y 12 caracteres")])
    password2= PasswordField('Repita su Contraseña', validators=[DataRequired(message="Dato requerido"),EqualTo('password', 'Las contraseñas ingresadas no coinciden')])
    submit = SubmitField('Registro')
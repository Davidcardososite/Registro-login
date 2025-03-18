from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from .models import User

class RegisterForm(FlaskForm):
    username = StringField('Usuário', validators=[InputRequired(), Length(min=4, max=25)])
    email = StringField('E-mail', validators=[InputRequired(), Email()])
    password = PasswordField('Senha', validators=[InputRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Senha', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Este e-mail já está registrado.')

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Este nome de usuário já está registrado.')

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[InputRequired(), Email()])
    password = PasswordField('Senha', validators=[InputRequired()])
    submit = SubmitField('Login')

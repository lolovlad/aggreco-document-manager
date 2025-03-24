from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Length, Email, DataRequired


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email()])
    password = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4, max=100)])
    remember = BooleanField("Запомнить: ", default=False)
    submit = SubmitField("Войти")
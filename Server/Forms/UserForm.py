from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FileField, SubmitField, HiddenField, PasswordField
from wtforms.validators import DataRequired, Optional, Email, ValidationError
from flask_wtf.file import FileAllowed


class UserForm(FlaskForm):
    id = HiddenField("id")
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    patronymics = StringField('Отчество', validators=[Optional()])
    id_role = SelectField('Роль', coerce=int, validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[Optional()])
    job_title = StringField('Должность', validators=[Optional()])
    submit = SubmitField('Сохранить')

    def validate_id_role(self, field):
        from flask_login import current_user
        user_roles = current_user.user.role.name
        if 'admin' in user_roles and field.data not in [2, 3]:
            raise ValidationError('Вы можете добавлять только обычных пользователей.')
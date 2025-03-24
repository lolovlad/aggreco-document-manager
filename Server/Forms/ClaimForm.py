from flask_wtf import FlaskForm
from wtforms import FileField, DateField, SubmitField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileAllowed


class ClaimForm(FlaskForm):
    id = HiddenField("id")
    description = TextAreaField('Коментарий', validators=[Optional()])
    file = FileField('Отчет', validators=[Optional(), FileAllowed(['docx'])])
    submit = SubmitField('Сохранить')
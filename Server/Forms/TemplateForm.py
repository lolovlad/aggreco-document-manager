from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FileField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileAllowed


class TemplateForm(FlaskForm):
    id = HiddenField("id")
    file = FileField('Загрузить шаблон', validators=[Optional(), FileAllowed(['docx'])])
    name = StringField('Название шаблона', validators=[DataRequired()])
    types = SelectField('Тип шаблона', coerce=int, validators=[DataRequired()])
    plant = SelectField('Тип устройства', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Добавить')
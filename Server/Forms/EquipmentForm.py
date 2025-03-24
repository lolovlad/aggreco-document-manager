from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, SubmitField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileAllowed


class EquipmentForm(FlaskForm):
    id = HiddenField("id")
    code = StringField('Код машины', validators=[DataRequired()])
    type = SelectField('Тип машины', coerce=int, choices=[])
    description = TextAreaField('Описание', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
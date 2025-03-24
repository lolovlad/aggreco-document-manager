from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class TypeDeviceForm(FlaskForm):
    type_device = StringField("Тип прибора: ", validators=[DataRequired()])
    submit = SubmitField("Сохранить")
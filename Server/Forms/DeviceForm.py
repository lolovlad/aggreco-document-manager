from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileAllowed


class DeviceForm(FlaskForm):
    id = HiddenField("id")
    name = StringField('Название', validators=[DataRequired()])
    type = SelectField('Тип прибора', coerce=int, choices=[])
    number = StringField('Заводской номер', validators=[DataRequired()])
    date_verification = DateField('Дата поверки', format='%Y-%m-%d', validators=[DataRequired()])
    date_next_verification = DateField('Дата следующей поверки', format='%Y-%m-%d', validators=[DataRequired()])
    certificate_number = StringField('Номер свидетельства', validators=[DataRequired()])
    submit = SubmitField('Созранить')
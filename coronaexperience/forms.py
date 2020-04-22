from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class TweetsUntilForm(FlaskForm):
    dateuntil = DateField("Until", format="%d-%m-%Y",validators=[DataRequired()])
    submit = SubmitField("Find")
    #hour = IntegerField("H",validators=[NumberRange(min=0, max=23)], default=0)
    #minute = IntegerField("M",validators=[NumberRange(min=0, max=59)],default=0)

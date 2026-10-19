from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField("Naam", validators=[DataRequired(), Length(max=100)])
    email = StringField("E-mail", validators=[DataRequired(), Email(check_deliverability=False), Length(max=200)])
    subject = StringField("Onderwerp", validators=[DataRequired(), Length(max=200)])
    message = TextAreaField("Bericht", validators=[DataRequired(), Length(max=5000)])

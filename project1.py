from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired

class TwitterForm(FlaskForm):
    twitter_name = StringField('twitter_name', validators=[InputRequired()])
    submit = SubmitField('sumbit')

    results = "asdfa"
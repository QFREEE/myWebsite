from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired
import twitterProject.RandomWriter as RandomWriter

class TwitterForm(FlaskForm):
    twitter_name = StringField('twitter_name', validators=[InputRequired()])
    submit = SubmitField('sumbit')

    # R = RandomWriter.RandomWriter(15)
    # R.train_tweets(twitter_name)
    # results = R.generate_tweets(100)

from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length

class PostForm(FlaskForm):
    is_dev = BooleanField('Dev Post')
    text = TextAreaField('Type here', validators=[DataRequired()])
    # SelectField does not allow None
    project = 'TDR'
    submit = SubmitField('Submit')

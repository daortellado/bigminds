from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import BooleanField, StringField, SubmitField, PasswordField, IntegerField, validators
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange
from wtforms_components import TimeField

class TimeForm(FlaskForm):
	classname = StringField('Class Name')
	time = TimeField('Time')
	dow = IntegerField('Day of Week', [validators.NumberRange(min=0, max=6)])
	zoomlink = StringField('Link')
	submit_1 = SubmitField('Update')

class AppSettingsForm(FlaskForm):
    chat_enabled = BooleanField('Chat enabled?')
    homepage_title = StringField('Homepage Title')
    hex_value = StringField('6 digit hex code for home background color...')
    submit_1 = SubmitField('Update')

class MediaFileUploadForm(FlaskForm):
    media_file = FileField('Media file to display on home page...', validators=[FileAllowed(['jpg', 'png', 'gif',
                                                                                             'webm', 'mp4'])])
    submit_2 = SubmitField('Submit')

class LoginForm(FlaskForm):
    """User Login Form."""
    email = StringField('Email')
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    # validators=[DataRequired(),
    #                                          Email(message='Enter a valid email.')]
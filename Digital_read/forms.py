from flask_wtf import FlaskForm, RecaptchaField
from wtforms import Form, StringField, PasswordField, SubmitField, FileField, TextAreaField, IntegerField, SelectField, TelField
from wtforms.validators import Email, DataRequired, URL
from flask_wtf.file import FileField, FileAllowed, FileRequired, FileSize

entry = '🤨Please Enter Verification Code!'
file_entry = '🤨 field must be filled!'
e_mail = '🐒 Enter a valid Email!'
link = '🐒 Enter a valid link!!'
file_error = '📁This file format cannot be accepted!'

class Verification(FlaskForm):
	card_number = StringField('Card_number')
	password = PasswordField('Verification Code')
	submit = SubmitField('Grant Access!')
	
class Pals_Form(FlaskForm):
	text = TextAreaField('Messege', validators=[DataRequired("can't send empty space")])
#	copies = IntegerField('How many copies?', validators=[DataRequired(entry)])
#	email = StringField('Email', validators=[DataRequired(entry), Email(e_mail)])
#	password = PasswordField('Password', validators=[DataRequired(entry)])
	submit = SubmitField('Send')


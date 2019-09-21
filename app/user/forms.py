from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class EditProfileForm(FlaskForm):
	first_name = StringField('First Name', validators=[DataRequired()])
	last_name = StringField('Last Name', validators=[DataRequired()])
	blurb = TextAreaField('Blurb', validators=[Length(min=0, max=1024)])

	skill_pm = BooleanField('Project Management')
	skill_pr = BooleanField('Programming')
	skill_gd = BooleanField('Graphic Design')
	skill_cm = BooleanField('Communication')
	skill_bs = BooleanField('Business')

	submit = SubmitField('Submit')
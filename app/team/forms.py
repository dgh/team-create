from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class TeamCreateForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(min=1, max=128)])
	blurb = TextAreaField('Description', validators=[Length(min=0, max=1024)])
	
	skill_pm = BooleanField('Project Management')
	skill_pr = BooleanField('Programming')
	skill_gd = BooleanField('Graphic Design')
	skill_cm = BooleanField('Communication')
	skill_bs = BooleanField('Business')

	submit = SubmitField('Create')

class TeamDeleteForm(FlaskForm):
	submit = SubmitField('Delete Team')
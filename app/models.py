from datetime import datetime
from hashlib import md5
from time import time
import json
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login

'''
After modifying the model run
	flask db migrate
to generate a new migration script.

Review the changes and then apply them with
	flask db upgrade
'''

@login.user_loader
def load_user(id):
	return User.query.get(int(id))


members = db.Table('members',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, index=True, primary_key=True)
	email = db.Column(db.String(128), index=True, unique=True)

	first_name = db.Column(db.String(64))
	last_name = db.Column(db.String(64))
	
	password_hash = db.Column(db.String(128))
	blurb = db.Column(db.String(1024))
	
	skill_pm = db.Column(db.Boolean, default=False)
	skill_pr = db.Column(db.Boolean, default=False)
	skill_gd = db.Column(db.Boolean, default=False)
	skill_cm = db.Column(db.Boolean, default=False)
	skill_bs = db.Column(db.Boolean, default=False)

	messages_sent = db.relationship('Message', foreign_keys='Message.sender_id',
									backref='author', lazy='dynamic')
	messages_received = db.relationship('Message', foreign_keys='Message.recipient_id',
										backref='recipient', lazy='dynamic')
	
	def get_fullname(self):
		return self.first_name + " " + self.last_name

	def get_skills(self):
		return [('Project Management', self.skill_pm), ('Programming', self.skill_pr),
				('Graphic Design', self.skill_gd), ('Communication', self.skill_cm),
				('Business', self.skill_bs)]

	def get_aquired_skills(self):
		skill_list = [('Project Management', self.skill_pm), ('Programming', self.skill_pr),
					  ('Graphic Design', self.skill_gd), ('Communication', self.skill_cm),
					  ('Business', self.skill_bs)]
		needed_skills = []
		for skill in skill_list:
			if skill[1]:
				needed_skills.append(skill)
		return needed_skills

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def avatar(self, size):
		digest = md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&size={}'.format(digest, size)

class Team(db.Model):
	id = db.Column(db.Integer, index=True, primary_key=True)
	owner = db.Column(db.Integer, db.ForeignKey('user.id'))
	members = db.relationship("User", secondary=members, backref=db.backref('teams', lazy='dynamic'))
	blurb = db.Column(db.String(1024))
	name = db.Column(db.String(128))

	skill_pm = db.Column(db.Boolean, default=False)
	skill_pr = db.Column(db.Boolean, default=False)
	skill_gd = db.Column(db.Boolean, default=False)
	skill_cm = db.Column(db.Boolean, default=False)
	skill_bs = db.Column(db.Boolean, default=False)

	def get_skills(self):
		return [('Project Management', self.skill_pm), ('Programming', self.skill_pr),
				('Graphic Design', self.skill_gd), ('Communication', self.skill_cm),
				('Business', self.skill_bs)]

	def get_needed_skills(self):
		skill_list = [('Project Management', self.skill_pm), ('Programming', self.skill_pr),
					  ('Graphic Design', self.skill_gd), ('Communication', self.skill_cm),
					  ('Business', self.skill_bs)]
		needed_skills = []
		for skill in skill_list:
			if skill[1]:
				needed_skills.append(skill)
		return needed_skills

	def is_owner(self, user):
		return self.owner == user.id

	def is_member(self, user):
		return user in self.members

	def add_member(self, user):
		if not self.is_member(user):
			self.members.append(user)

	def remove_member(self, user):
		if self.is_member(user):
			self.members.remove(user)

class Message(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	body = db.Column(db.String(1024))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
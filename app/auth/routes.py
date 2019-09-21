from werkzeug.urls import url_parse
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from datetime import datetime
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User

@bp.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))

	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid email or password')
			return redirect(url_for('auth.login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('main.index')
		return redirect(next_page)

	return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
	logout_user()

	return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))

	form = RegistrationForm()

	if form.validate_on_submit():
		print("added")
		user = User(email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data)
		user.set_password(form.password.data)
		user.skill_pm = form.skill_pm.data
		user.skill_pr = form.skill_pr.data
		user.skill_gd = form.skill_gd.data
		user.skill_cm = form.skill_cm.data
		user.skill_bs = form.skill_bs.data
		print(user.get_skills())
		db.session.add(user)
		db.session.commit()
		flash('Registration complete! Welcome {} {}'.format(form.first_name.data, form.last_name.data))
		return redirect(url_for('auth.login'))

	return render_template('auth/register.html', title='Register', form=form)
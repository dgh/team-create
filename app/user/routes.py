from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import db
from app.user import bp
from app.user.forms import EditProfileForm
from app.models import User

@bp.route('/<userid>')
def user(userid):
	user = User.query.filter_by(id=userid).first_or_404()
	fullname = user.first_name  + " " + user.last_name

	return render_template('user/user.html', title=fullname, user=user)

@bp.route('/<userid>/edit', methods=['GET', 'POST'])
@login_required
def user_edit(userid):
	if current_user.id != int(userid):
		flash('You can only edit your own profile')
		return redirect(url_for('user.user', userid=current_user.id))

	form = EditProfileForm()

	if form.validate_on_submit():
		current_user.first_name = form.first_name.data
		current_user.last_name = form.last_name.data
		current_user.blurb = form.blurb.data
		current_user.skill_pm =	form.skill_pm.data
		current_user.skill_pr = form.skill_pr.data
		current_user.skill_gd = form.skill_gd.data
		current_user.skill_cm = form.skill_cm.data
		current_user.skill_bs = form.skill_bs.data

		db.session.commit()
		flash('Your changes have been saved')
		return redirect(url_for('user.user', userid=current_user.id))

	elif request.method == 'GET':
		form.first_name.data = current_user.first_name
		form.last_name.data = current_user.last_name
		form.blurb.data = current_user.blurb
		form.skill_pm.data = current_user.skill_pm
		form.skill_pr.data = current_user.skill_pr
		form.skill_gd.data = current_user.skill_gd
		form.skill_cm.data = current_user.skill_cm
		form.skill_bs.data = current_user.skill_bs
		
	return render_template('user/edit.html', title='Edit Profile', form=form)
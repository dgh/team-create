from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user, login_required
from app import db
from app import db
from app.team import bp
from app.team.forms import TeamCreateForm, TeamDeleteForm
from app.models import User, Team

@bp.route('/<teamid>')
def team(teamid):
	team = Team.query.filter_by(id=teamid).first_or_404()
	owner = User.query.filter_by(id=team.owner).first_or_404()

	return render_template('team/team.html', title=team.name, team=team, owner=owner)

@bp.route('/my-teams')
@login_required
def my_teams():
	page = request.args.get('page', 1, type=int)
	teams = current_user.teams.order_by(Team.id).paginate(
		page, current_app.config['POSTS_PER_PAGE'], False)

	next_url = url_for('team.my_teams', page=teams.next_num) \
		if teams.has_next else None
	prev_url = url_for('team.my_teams', page=teams.prev_num) \
		if teams.has_prev else None

	return render_template('team/my_teams.html', title='My Teams', teams=teams.items,
							next_url=next_url, prev_url=prev_url)

@bp.route('/<teamid>/edit', methods=['GET', 'POST'])
@login_required
def edit(teamid):
	team = Team.query.filter_by(id=teamid).first_or_404()
	
	if not team.is_owner(current_user):
		flash('You can\'t edit a team you don\'t own')
		return redirect(url_for('team.team', teamid=teamid))

	form1 = TeamCreateForm(prefix="form1")
	form2 = TeamDeleteForm(prefix="form2")

	if form1.validate_on_submit():
		team.name = form1.name.data
		team.blurb = form1.blurb.data
		team.skill_pm =	form1.skill_pm.data
		team.skill_pr = form1.skill_pr.data
		team.skill_gd = form1.skill_gd.data
		team.skill_cm = form1.skill_cm.data
		team.skill_bs = form1.skill_bs.data

		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('team.team', teamid=teamid))

	elif request.method == 'GET':
		print("ehh")
		form1.name.data = team.name
		form1.blurb.data = team.blurb
		form1.skill_pm.data = team.skill_pm
		form1.skill_pr.data = team.skill_pr
		form1.skill_gd.data = team.skill_gd
		form1.skill_cm.data = team.skill_cm
		form1.skill_bs.data = team.skill_bs

	if form2.validate_on_submit():
		flash('{} has been deleted'.format(team.name))
		db.session.delete(team)
		db.session.commit()
		return redirect(url_for('team.my_teams'))

	return render_template('team/edit.html', title='Edit Team', team=team, form1=form1, form2=form2)

@bp.route('/<teamid>/join')
@login_required
def join(teamid):
	team = Team.query.filter_by(id=teamid).first_or_404()

	if team.is_member(current_user):
		flash('You\'re already a member')
		return redirect(url_for('team.team', teamid=teamid))

	team.add_member(current_user)
	db.session.commit()

	flash('You have joined {}'.format(team.name))
	return redirect(url_for('team.team', teamid=teamid))

@bp.route('/<teamid>/leave')
@login_required
def leave(teamid):
	team = Team.query.filter_by(id=teamid).first_or_404()

	if team.is_owner(current_user):
		flash('You can not leave your own team')
		return redirect(url_for('team.team', teamid=teamid)) 

	if not team.is_member(current_user):
		flash('You\'re not a member of this team')
		return redirect(url_for('team.team', teamid=teamid))
	
	team.remove_member(current_user)
	db.session.commit()

	flash('You have left {}'.format(team.name))
	return redirect(url_for('team.team', teamid=teamid))
	

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
	form = TeamCreateForm()

	if form.validate_on_submit():
		print("added")
		team = Team(owner=current_user.id, name=form.name.data, blurb=form.blurb.data)
		team.skill_pm = form.skill_pm.data
		team.skill_pr = form.skill_pr.data
		team.skill_gd = form.skill_gd.data
		team.skill_cm = form.skill_cm.data
		team.skill_bs = form.skill_bs.data
		team.add_member(current_user)
		db.session.add(team)
		db.session.commit()
		flash('Your team {} was created!'.format(form.name.data))
		return redirect(url_for('team.team', teamid=team.id))

	return render_template('team/create.html', title='Create Team', form=form)

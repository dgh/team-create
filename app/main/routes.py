from werkzeug.urls import url_parse
from flask import render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import current_user, login_required
from datetime import datetime
from app import db
from app.main.forms import MessageForm
from app.models import User, Message, Team
from app.main import bp

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
	page = request.args.get('page', 1, type=int)
	teams = Team.query.order_by(Team.id).paginate(
		page, 3, False)

	next_url = url_for('main.index', page=teams.next_num) \
		if teams.has_next else None
	prev_url = url_for('main.index', page=teams.prev_num) \
		if teams.has_prev else None

	return render_template('index.html', title='Home', teams=teams.items,
							next_url=next_url, prev_url=prev_url)

@bp.route('/teams')
def teams():
	page = request.args.get('page', 1, type=int)
	teams = Team.query.order_by(Team.id).paginate(
		page, current_app.config['POSTS_PER_PAGE'], False)

	next_url = url_for('main.teams', page=teams.next_num) \
		if teams.has_next else None
	prev_url = url_for('main.teams', page=teams.prev_num) \
		if teams.has_prev else None

	return render_template('teams.html', title='Teams', teams=teams.items,
							next_url=next_url, prev_url=prev_url)

@bp.route('/members')
def members():
	page = request.args.get('page', 1, type=int)
	users = User.query.order_by(User.id).paginate(
		page, current_app.config['POSTS_PER_PAGE'], False)

	next_url = url_for('main.members', page=users.next_num) \
		if users.has_next else None
	prev_url = url_for('main.members', page=users.prev_num) \
		if users.has_prev else None

	return render_template('members.html', title='Members', users=users.items,
							next_url=next_url, prev_url=prev_url)

@bp.route('/compose/<id>', methods=['GET', 'POST'])
@login_required
def compose(id):
	recipient = User.query.filter_by(id=id).first_or_404()
	form = MessageForm()

	if current_user == recipient:
		flash('You can\'t send yourself a message')
		return redirect(url_for('user.user', userid=current_user.id))

	if form.validate_on_submit():
		msg = Message(author=current_user, recipient=recipient, body=form.message.data)
		db.session.add(msg)
		db.session.commit()
		flash('Your message has been sent')
		return redirect(url_for('user.user', userid=id))

	print("no send")
	return render_template('compose.html', title='Send Message', form=form, recipient=recipient)

@bp.route('/messages')
@login_required
def messages():
	page = request.args.get('page', 1, type=int)
	messages = current_user.messages_received.order_by(Message.timestamp.desc()).paginate(
				page, current_app.config['POSTS_PER_PAGE'], False)

	next_url = url_for('main.messages', page=messages.next_num) \
		if messages.has_next else None
	prev_url = url_for('main.messages', page=messages.prev_num) \
		if messages.has_prev else None

	return render_template('messages.html', title="Messages", messages=messages.items,
							next_url=next_url, prev_url=prev_url)
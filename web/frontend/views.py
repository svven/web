# -*- coding: utf-8 -*-


from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session)
from flask.ext.login import login_required, login_user, current_user, logout_user

from forms import SignupForm, LoginForm
from ..extensions import db
from ..auth.models import User


frontend = Blueprint('frontend', __name__)


@frontend.route('/')
def index():
	current_app.logger.debug('debug')

	if current_user.is_authenticated():
		return redirect(url_for('user.index'))

	return render_template('index.html')


@frontend.route('/signup', methods=['GET', 'POST'])
def signup():
	if current_user.is_authenticated():
		return redirect(url_for('user.index'))

	form = SignupForm(next=request.args.get('next'))

	if form.validate_on_submit():
		user = User()
		form.populate_obj(user)

		db.session.add(user)
		db.session.commit()

		if login_user(user):
			return redirect(form.next.data or url_for('user.index'))

	return render_template('frontend/signup.html', form=form)


@frontend.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated():
		return redirect(url_for('user.index'))

	form = LoginForm(login=request.args.get('login', None),
	                 next=request.args.get('next', None))

	if form.validate_on_submit():
		user, authenticated = User.authenticate(form.login.data,
		                                        form.password.data)

		if user and authenticated:
			remember = request.form.get('remember') == 'y'
			if login_user(user, remember=remember):
				flash("Logged in", 'success')
				session['username'] = request.form['username']
			return redirect(form.next.data or url_for('user.index'))
		else:
			flash('Sorry, invalid login', 'error')

	return render_template('frontend/login.html', form=form)


@frontend.route('/logout')
@login_required
def logout():
	logout_user()
	flash('Logged out', 'success')
	return redirect(url_for('frontend.index'))


@frontend.route('/help')
def help():
	return render_template('frontend/footers/help.html', active="help")


@frontend.route('/terms')
def terms():
	return render_template('frontend/terms.html', active="help")

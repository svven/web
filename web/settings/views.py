# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash
from flask.ext.login import login_required, current_user

from ..extensions import db
from ..user import User
from .forms import ProfileForm, PasswordForm


settings = Blueprint('settings', __name__, url_prefix='/settings')


@settings.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	user = User.query.filter_by(name=current_user.name).first_or_404()
	form = ProfileForm(email=current_user.email,
	                   role_code=current_user.role_code,
	                   status_code=current_user.status_code,
	                   next=request.args.get('next'))

	if form.validate_on_submit():
		form.populate_obj(user)

		db.session.add(user)
		db.session.commit()

		flash('Public profile updated.', 'success')

	return render_template('settings/profile.html', user=user,
	                       active="profile", form=form)


@settings.route('/password', methods=['GET', 'POST'])
@login_required
def password():
	user = User.query.filter_by(name=current_user.name).first_or_404()
	form = PasswordForm(next=request.args.get('next'))

	if form.validate_on_submit():
		form.populate_obj(user)
		user.password = form.new_password.data

		db.session.add(user)
		db.session.commit()

		flash('Password updated.', 'success')

	return render_template('settings/password.html', user=user,
	                       active="password", form=form)

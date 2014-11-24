# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash
from flask.ext.login import login_required, current_user

from ..extensions import db
from ..auth import User
from .forms import ProfileForm


settings = Blueprint('settings', __name__, url_prefix='/settings')


@settings.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	user = User.query.filter_by(name=current_user.name).first_or_404()
	form = ProfileForm(next=request.args.get('next'))

	if form.validate_on_submit():
		form.populate_obj(user)

		db.session.add(user)
		db.session.commit()

		flash('Public profile updated.', 'success')

	return render_template('settings/profile.html', user=user,
	                       active="profile", form=form)



# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, abort
from flask.ext.login import login_required, current_user

from .models import User


user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/')
@login_required
def index():
	if not current_user.is_authenticated():
		abort(403)
	return render_template('user/index.html', user=current_user)


@user.route('/<string:screen_name>/')
def profile(screen_name):
	(svven_user, authenticated) = User.get_by_screen_name(screen_name)
	return render_template('user/profile.html', user=svven_user)


# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, abort
from flask.ext.login import login_required, current_user


user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/')
@login_required
def index():
    if not current_user.is_authenticated():
        abort(403)
    return render_template('user/index.html', user=current_user)


@user.route('/<int:user_id>/profile')
def profile(user_id):
    # user = User.get_by_id(user_id)
    return render_template('user/profile.html', user=user)

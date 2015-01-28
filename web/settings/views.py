# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash, abort
from flask.ext.login import login_required, current_user

from database.auth.models import User
from .forms import ProfileForm
from database import db


settings = Blueprint('settings', __name__, url_prefix='/settings')


@settings.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    s = db.Session()
    user = s.query(User).filter_by(name=current_user.name)
    if user is None:
        abort(404)
    form = ProfileForm(next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(user)
        s.add(user)
        s.commit()
        flash('Public profile updated.', 'success')

    return render_template('settings/profile.html', user=user,
                           active="profile", form=form)



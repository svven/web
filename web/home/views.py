"""
Home blueprint.
"""
from flask import Blueprint, \
    url_for, redirect, session, current_app
from flask.ext.login import login_required, current_user

from .. import db
from ..news.views import render_reader

home = Blueprint('home', __name__)

@home.route('/')
@login_required
def page():
    current_user.reader.refresh(db.session)
    return render_reader(current_user.reader)

@home.route('/tour/<tour_name>/')
@login_required
def tour(tour_name):
    session['tour'] = tour_name
    return redirect(url_for('home.page'))

"""
Front blueprint.
"""
from flask import Blueprint, render_template, \
    redirect, url_for
from flask.ext.login import login_required, current_user
from sqlalchemy.orm import joinedload, contains_eager

from .. import home
from database.models import *

front = Blueprint('front', __name__)

@front.route('/')
def page():
    if current_user.is_authenticated():
        # return redirect(url_for('home.page'))
        return home.page() # @login_required
    else:
        # return latest()
        return render_template('front/page.html')

@front.route('/latest')
def latest():
    # readers = Reader.query.join(TwitterUser).\
        # options(contains_eager(Reader.twitter_user)).\
        # order_by(TwitterUser.screen_name).all() # temporary
    marks = Mark.query.\
        join(Status, Link, Reader, TwitterUser).options(
            contains_eager(Mark.twitter_status),
            contains_eager(Mark.link),
            contains_eager(Mark.reader, Reader.twitter_user)).\
        order_by(Status.created_at.desc()).limit(30)
    return render_template('news/latest.html', 
        marks=marks)
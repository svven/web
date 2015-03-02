"""
Home blueprint.
"""
from flask import Blueprint, render_template

from sqlalchemy.orm import joinedload, contains_eager

from database.models import *

home = Blueprint('home', __name__)

@home.route('/')
def page():
    readers = Reader.query.join(TwitterUser).\
        options(contains_eager(Reader.twitter_user)).\
        order_by(TwitterUser.screen_name).all() # temporary

    marks = Mark.query.\
        join(Status, Link, Reader, TwitterUser).options(
            contains_eager(Mark.twitter_status),
            contains_eager(Mark.link),
            contains_eager(Mark.reader, Reader.twitter_user)).\
        order_by(Status.created_at.desc()).limit(30)
    return render_template('news/marks.html',
        marks=marks, readers=readers)

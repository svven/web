"""
Home blueprint.
"""
from flask import Blueprint, render_template

from sqlalchemy.orm import joinedload, contains_eager

from database.auth import *
from database.news import *
from database.twitter import *

home = Blueprint('home', __name__)

@home.route('/')
def page():
    readers = Reader.query.join(User).\
        options(contains_eager(Reader.twitter_user)).\
        order_by(User.screen_name).all() # temporary

    marks = Mark.query.\
        join(Status, Link, Reader, User).options(
            contains_eager(Mark.link),
            contains_eager(Mark.reader, Reader.twitter_user)).\
        order_by(Status.created_at.desc()).limit(15)
    return render_template('reader/marks.html',
        marks=marks, readers=readers)

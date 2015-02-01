"""
Reader blueprint.
"""
from flask import Blueprint, render_template

from sqlalchemy.orm import joinedload, contains_eager

from database.news import *
from database.twitter import *

reader = Blueprint('reader', __name__)

@reader.route('/@<screen_name>')
def marks(screen_name):
    readers = Reader.query.join(User).\
        options(contains_eager(Reader.twitter_user)).\
        order_by(User.screen_name).all() # temporary

    user = User.query.filter_by(screen_name=screen_name).first()
    if user and user.reader:
        marks = user.reader.marks.\
            join(Status, Link).options(
                contains_eager(Mark.twitter_status),
                contains_eager(Mark.link)).\
            order_by(Mark.moment.desc()).limit(30)
    else:
        marks = []
    return render_template('reader/marks.html', 
        user=user, marks=marks, readers=readers)

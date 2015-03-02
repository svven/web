"""
News blueprint.
"""
from flask import Blueprint, render_template

from sqlalchemy.orm import joinedload, contains_eager

from database.models import *

news = Blueprint('news', __name__)

@news.route('/@<screen_name>')
def marks(screen_name):
    readers = Reader.query.join(TwitterUser).\
        options(contains_eager(Reader.twitter_user)).\
        order_by(TwitterUser.screen_name).all() # temporary

    user = TwitterUser.query.filter_by(screen_name=screen_name).first()
    if user and user.reader:
        marks = user.reader.marks.\
            join(Status, Link).options(
                contains_eager(Mark.twitter_status),
                contains_eager(Mark.link)).\
            order_by(Mark.moment.desc()).limit(30)
    else:
        marks = []
    return render_template('news/marks.html', 
        user=user, marks=marks, readers=readers)

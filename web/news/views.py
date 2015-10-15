"""
News blueprint.
"""
from flask import Markup, Blueprint, render_template, abort, flash
from flask.ext.login import login_required, current_user
from sqlalchemy.orm import joinedload, contains_eager

from models import WebReader
from database.models import TwitterUser
from aggregator.utils import munixtime

news = Blueprint('news', __name__)

import datetime
timeago = lambda **kvargs:\
    datetime.datetime.utcnow() - datetime.timedelta(**kvargs)

@news.route('/<screen_name>/')
@news.route('/@<screen_name>/')
@login_required
def reader(screen_name):
    reader = WebReader.query.\
        outerjoin(TwitterUser).options(
            contains_eager(WebReader.twitter_user)).\
        filter(TwitterUser.screen_name.ilike(screen_name)).first()
    if not reader:
        abort(404)
    ego = current_user.is_authenticated() and \
        current_user.screen_name == reader.screen_name
    if reader.ignored and not ego:
        abort(404)
    # reader.aggregate() # temp
    reader.set_fellows()
    reader.set_edition(moment_min=munixtime(timeago(hours=30)))
    reader.load()
    return render_template('news/reader.html', ego=ego, reader=reader)

# @news.route('/featured')
# @login_required
# def featured():
    # reader = current_user.reader
    # readers = WebReader.query.\
        # filter(WebReader.featured != None).\
        # order_by(WebReader.featured.desc()).limit(30)
    # return render_template('news/featured.html', reader=reader, readers=readers)
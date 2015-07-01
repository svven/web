"""
News blueprint.
"""
from flask import Markup, Blueprint, render_template, abort, flash
from flask.ext.login import login_required, current_user
from sqlalchemy.orm import joinedload, contains_eager

from database.models import *
from aggregator.mixes import *
from aggregator.utils import munixtime

news = Blueprint('news', __name__)

import datetime
timeago = lambda **kvargs:\
    datetime.datetime.utcnow() - datetime.timedelta(**kvargs)

@news.route('/<screen_name>/')
@news.route('/@<screen_name>/')
@login_required
def reader(screen_name):
    reader = MixedReader.query.\
        outerjoin(TwitterUser).options(
            contains_eager(MixedReader.twitter_user)).\
        filter(TwitterUser.screen_name.ilike(screen_name)).first()
    ego = current_user.is_authenticated() and \
        current_user.screen_name == reader.screen_name
    if not reader or (reader.ignored and not ego):
        abort(404)
    # reader.aggregate() # temp
    reader.set_fellows()
    reader.set_edition(moment_min=munixtime(timeago(hours=30)))
    reader.load()
    return render_template('news/reader.html', ego=ego, reader=reader)

@news.route('/featured')
@login_required
def featured():
    readers = MixedReader.query.\
        filter(Reader.featured != None).\
        order_by(Reader.featured.desc()).limit(30)
    return render_template('news/featured.html', readers=readers)
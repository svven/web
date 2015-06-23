"""
News blueprint.
"""
from flask import Blueprint, render_template, abort
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
    if not reader:
        abort(404)
    
    # reader.aggregate() # temp
    reader.set_fellows()
    reader.set_edition() # moment_min=munixtime(timeago(days=3)))
    
    picks = reader.picks
    fellows = reader.fellows
    edition = reader.edition
    
    ego = current_user.is_authenticated() and \
        current_user.screen_name == reader.screen_name

    return render_template('news/reader.html', ego=ego, 
        reader=reader, edition=edition, fellows=fellows, picks=picks)

"""
News blueprint.
"""
from flask import Blueprint, render_template, abort
from flask.ext.login import login_required
from sqlalchemy.orm import joinedload, contains_eager

from database.models import *
from aggregator.mixes import *
from aggregator.utils import munixtime

news = Blueprint('news', __name__)

import datetime
timeago = lambda **kvargs:\
    datetime.datetime.utcnow() - datetime.timedelta(**kvargs)

@news.route('/@<screen_name>/')
@login_required
def edition(screen_name):
    reader = MixedReader.query.\
        outerjoin(TwitterUser).options(
            contains_eager(MixedReader.twitter_user)).\
        filter(TwitterUser.screen_name.ilike(screen_name)).first()
    if not reader:
        abort(404)
    
    # reader.aggregate() # temp
    reader.set_fellows()
    reader.set_edition(moment_min=munixtime(timeago(days=1)))
    
    fellows = reader.fellows
    edition = reader.edition
    
    for link in edition:
        markers_ids = link.get_markers()
        link.fellows = [f for f in fellows if str(f.id) in markers_ids]
    
    return render_template('news/edition.html', 
        reader=reader, edition=edition, fellows=fellows)

@news.route('/@<screen_name>/marks')
def marks(screen_name):
    reader = MixedReader.query.\
        outerjoin(TwitterUser).options(
            contains_eager(MixedReader.twitter_user)).\
        filter(TwitterUser.screen_name.ilike(screen_name)).first()
    if not reader:
        abort(404)
    
    marks = reader.marks.\
        join(Status, Link).options(
            contains_eager(Mark.twitter_status),
            contains_eager(Mark.link)).\
        order_by(Mark.moment.desc()).limit(30)
    return render_template('news/edition.html', 
        reader=reader, marks=marks)

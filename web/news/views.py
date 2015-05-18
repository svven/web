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

    # marks = reader.marks.\
    #     join(Status, Link).options(
    #         contains_eager(Mark.twitter_status),
    #         contains_eager(Mark.link)).\
    #     order_by(Mark.moment.desc()).limit(30)
    marks = reader.marks
    
    # reader.aggregate() # temp
    reader.set_fellows()
    reader.set_edition(moment_min=munixtime(timeago(days=3)))
    
    fellows = reader.fellows
    edition = reader.edition
    
    fellows_dict = {str(f.id): f for f in fellows}
    for link in edition:
        link.fellows = [fellows_dict[fid] for fid in link.fellows_ids]

    ego = current_user.is_authenticated() and \
        current_user.screen_name == reader.screen_name

    return render_template('news/reader.html', ego=ego, 
        reader=reader, edition=edition, fellows=fellows, marks=marks)

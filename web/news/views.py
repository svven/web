"""
News blueprint.
"""
from flask import Blueprint, render_template, abort
from sqlalchemy.orm import joinedload, contains_eager

from database.models import *
from aggregator.mixes import *

news = Blueprint('news', __name__)

@news.route('/@<screen_name>/marks')
def marks(screen_name):
    reader = MixedReader.query.\
        join(TwitterUser).options(
            contains_eager(MixedReader.twitter_user)).\
        filter(TwitterUser.screen_name == screen_name).first()
    if not reader:
        abort(404)
    
    marks = reader.marks.\
        join(Status, Link).options(
            contains_eager(Mark.twitter_status),
            contains_eager(Mark.link)).\
        order_by(Mark.moment.desc()).limit(30)
    return render_template('news/edition.html', 
        reader=reader, marks=marks)

@news.route('/@<screen_name>/edition')
def edition(screen_name):
    reader = MixedReader.query.\
        join(TwitterUser).options(
            contains_eager(MixedReader.twitter_user)).\
        filter(TwitterUser.screen_name == screen_name).first()
    if not reader:
        abort(404)
    
    reader.aggregate() # temp
    edition = reader.edition.all()
    fellows = reader.fellows.options(
        joinedload(MixedReader.auth_user),
        joinedload(MixedReader.twitter_user)).all()
    
    for link in edition:
        markers_ids = link.get_markers()
        link.fellows = [f for f in fellows if str(f.id) in markers_ids]
    return render_template('news/edition.html', 
        reader=reader, edition=edition, fellows=fellows)

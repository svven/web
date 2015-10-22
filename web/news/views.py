"""
News blueprint.
"""
from flask import Markup, Blueprint, render_template, abort, flash
from flask.ext.login import login_required, current_user
from sqlalchemy.orm import joinedload, contains_eager

from models import WebReader
from database.models import TwitterUser

news = Blueprint('news', __name__)

def get_reader(screen_name):
    return WebReader.query.\
        outerjoin(TwitterUser).options(
            contains_eager(WebReader.twitter_user)).\
        filter(TwitterUser.screen_name.ilike(screen_name)).first()
    
def render_reader(reader):
    if not reader:
        abort(404)
    if reader.ignored and not reader.is_current_user:
        abort(404)
    reader.reload()
    return render_template('news/reader.html', reader=reader)
    
    
@news.route('/<screen_name>/')
@news.route('/@<screen_name>/')
@login_required
def reader(screen_name):
    reader = get_reader(screen_name)
    return render_reader(reader)

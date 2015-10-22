"""
News blueprint.
"""
from flask import Blueprint, \
    render_template, abort
from flask.ext.login import login_required, current_user

from models import get_reader

news = Blueprint('news', __name__)
    
def render_reader(reader):
    if not reader or \
        (reader.ignored and not reader.is_current_user):
        abort(404)
    reader.reload() # every time
    return render_template('news/reader.html', reader=reader)
    
    
@news.route('/<screen_name>/')
@news.route('/@<screen_name>/')
@login_required
def reader(screen_name):
    reader = get_reader(screen_name)
    return render_reader(reader)

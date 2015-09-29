"""
Home blueprint.
"""
from flask import Blueprint, render_template
from flask.ext.login import login_required, current_user

from .. import news

home = Blueprint('home', __name__)

@home.route('/')
@login_required
def page():
    # return "Hey %s." % current_user.screen_name
    
    return news.reader(current_user.screen_name)
"""
Home blueprint.
"""
from flask import Blueprint, render_template
from flask.ext.login import login_required, current_user
from sqlalchemy.orm import joinedload, contains_eager

from .. import news
from database.models import *
from aggregator.mixes import *

home = Blueprint('home', __name__)

@home.route('/')
@login_required
def page():
    # return "Hey %s." % current_user.screen_name
    
    return news.edition(current_user.screen_name)
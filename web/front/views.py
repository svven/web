"""
Front blueprint.
"""
from flask import Blueprint, render_template, \
    redirect, url_for
from flask.ext.login import login_required, current_user
from sqlalchemy.orm import joinedload, contains_eager

from .. import home
from database.models import *

front = Blueprint('front', __name__)

@front.route('/')
def page():
    if current_user.is_authenticated():
        # return redirect(url_for('home.page'))
        return home.page() # @login_required
    else:
        return render_template('front/page.html')

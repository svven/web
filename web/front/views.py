"""
Front blueprint.
"""
from flask import Blueprint, \
    render_template, url_for, redirect
from flask.ext.login import login_required, current_user

from .. import home

front = Blueprint('front', __name__)

@front.route('/')
def page():
    if current_user.is_authenticated():
        # return redirect(url_for('home.page'))
        return home.page() # @login_required
    else:
        return render_template('front/page.html')

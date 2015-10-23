"""
Auth blueprint.
"""
from datetime import datetime
from flask import Blueprint, Markup, \
    current_app, request, flash, url_for, redirect, session
from flask.ext.login import LoginManager, \
    login_user, login_required, logout_user, current_user

from .. import db
from oauth import OAuth
from models import WebUser

auth = Blueprint('auth', __name__)
login_manager = LoginManager()

@login_manager.user_loader
def load_user(id):
    return WebUser.query.get(int(id))

@auth.record_once
def on_load(state):
    login_manager.login_view = 'auth.login'
    login_manager.login_message = None
    login_manager.init_app(state.app)

@auth.route('/authorize/<provider_name>')
def oauth_authorize(provider_name):
    if not current_user.is_anonymous():
        return redirect(url_for('home.page'))
    oauth = OAuth.get_provider(provider_name)
    return oauth.authorize()

@auth.route('/callback/<provider_name>')
def oauth_callback(provider_name):
    if not current_user.is_anonymous():
        return redirect(url_for('home.page'))
    oauth = OAuth.get_provider(provider_name)
    try:
        user_credentials = oauth.callback()
        if user_credentials is None:
            raise
    except Exception, e:
        current_app.logger.exception(e)
        flash('Oops, could not authenticate you, sorry.', 'danger')
        return redirect(url_for('front.page'))
    return authenticate(provider_name, user_credentials)

@auth.route('/signup')
def signup():
    return login()

@auth.route('/login')
def login():
    return redirect(url_for('.oauth_authorize', provider_name='twitter'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('front.page'))

def authenticate(provider_name, user_credentials):
    user, key, secret = user_credentials
    
    # private beta check - to be removed when going public
    if not WebUser.exists(provider_name, *user_credentials):
        message = Markup(
            '''Hey sorry you're not on the list.<br />
            <a class="alert-link" href="mailto:ducu@svven.com">Drop us a line</a> 
            if you want private beta access.''')
        flash(message, 'warning')
        current_app.logger.warning(
            'Blocked signup: %s (%s, %s)', user.screen_name, key, secret)
        return redirect(url_for('front.page'))
    user, created = WebUser.authenticate(provider_name, *user_credentials)
    first_time = created or not user.last_login_at
    
    login_user(user) # , remember=True
    login_tracking(user)
    
    if first_time:
        session['refresh'] = True
        current_app.logger.info(
            'Accepted signup: %s', user.screen_name)
        return redirect(url_for('home.tour', tour_name='welcome'))
    else:
        return redirect(url_for('home.page'))

def login_tracking(user):
    "Update login tracking data."
    if 'X-Forwarded-For' in request.headers:
        # See http://esd.io/blog/flask-apps-heroku-real-ip-spoofing.html
        addresses = request.headers.getlist("X-Forwarded-For")
        remote_addr = addresses and addresses[0] or 'untrackable'
    else:
        remote_addr = request.remote_addr or 'untrackable'
    if not user.last_login_at: # first time
        user.registered_at = datetime.utcnow()
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = remote_addr
    user.login_count = user.login_count and user.login_count + 1 or 1
    db.session.merge(user)
    db.session.commit()

"""
Auth blueprint.
"""
from flask import Blueprint, render_template, \
    current_app, request, flash, url_for, redirect, session, abort
from flask.ext.login import LoginManager, \
    login_user, login_required, logout_user, current_user

from oauth import OAuth
from models import User

auth = Blueprint('auth', __name__)
login_manager = LoginManager()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@auth.record_once
def on_load(state):
    login_manager.login_view = 'auth.login'
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
    user_credentials = oauth.callback()
    if user_credentials is None:
        return 'Not authorized.'
    user = User.authenticate(provider_name, *user_credentials)
    login_user(user, True)
    return redirect(url_for('home.page'))

@auth.route('/login')
def login():
    return redirect(url_for('.oauth_authorize', provider_name='twitter'))

@auth.route('/logout')
def logout():
    logout_user()
    return 'Logged out.'


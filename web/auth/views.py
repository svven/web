"""
Auth blueprint.
"""
from flask import Blueprint, current_app
from flask.ext.login import UserMixin, LoginManager, \
    login_user, logout_user, current_user

from oauth import OAuth
from database.auth.models import User as AuthUser
from database.twitter.models import User as TwitterUser

class User(UserMixin, AuthUser):
    pass

auth = Blueprint('auth', __name__)
login = LoginManager(current_app)

@login.user_loader
def load_user(id):
    return User.query.get(id)

@auth.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('page'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@auth.route('/callback/<provider>')
def oauth_callback(provider):
    # TODO
    pass

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('page'))

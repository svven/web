"""
Auth models.
"""
from flask.ext.login import UserMixin

from .. import db
from database.news.models import Reader
from database.auth.models import User as AuthUser
from database.twitter.models import User as TwitterUser, Token, Timeline

class User(AuthUser, UserMixin):
    "Svven user."

    @classmethod
    def authenticate(cls, provider_name, user, key, secret):
        "Authenticate based on provider user credentials."
        assert provider_name == 'twitter' # yet
        user_id, screen_name, user_data = (user.id, user.screen_name, user)
        print user_id, screen_name
        user = TwitterUser.query.filter_by(user_id=user_id).first() # twitter_user
        if not user: # new
            user = TwitterUser(user_data, key, secret)
            db.session.add(user)
        else: # exists
            user.load(user_data) # update
            user = db.session.merge(user)
            if not user.token:
                user.token = Token(user_id=user_id, key=key, secret=secret)
            else: # update access token
                user.token.key = key
                user.token.secret = secret
            if not user.timeline:
                user.timeline = Timeline(user_id=user_id)
        db.session.commit() # atomic
        user = User.query.filter_by(screen_name=screen_name).first()
        if not user: # new
            user = User(user_data) # auth_user
            db.session.add(user)
        else: # exists
            user.load(user_data) # update
            user = db.session.merge(user)
        db.session.commit() # atomic
        reader = Reader.query.filter_by(twitter_user_id=user_id).first() # reader
        if not reader: # new
            reader = Reader(twitter_user_id=user_id)
            db.session.add(reader)
        else:
            reader = db.session.merge(reader)
        reader.auth_user_id = user.id
        db.session.commit() # atomic
        return user

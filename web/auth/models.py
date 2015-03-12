"""
Auth models.
"""
from flask.ext.login import UserMixin

from .. import db
from database.auth.models import User as AuthUser
from database.twitter.models import User as TwitterUser, Token, Timeline

from aggregator.mixes import MixedReader

class User(AuthUser, UserMixin):
    "Svven User."

    @classmethod
    def authenticate(cls, provider_name, user, key, secret):
        "Authenticate based on provider user credentials."
        assert provider_name == 'twitter' # yet
        auth_user = User.register_auth_user(user)
        twitter_user = User.register_twitter_user(user, key, secret)
        news_reader = User.register_news_reader(auth_user, twitter_user)
        return auth_user

    @classmethod
    def register_auth_user(cls, user):
        "Get or create specified Svven Auth User."
        screen_name, user_data = (user.screen_name, user)
        user = User.query.filter_by(screen_name=screen_name).first()
        if not user: # new
            user = User(user_data) # auth_user
            db.session.add(user)
        else: # exists
            user.load(user_data) # update
            user = db.session.merge(user)
        db.session.commit()
        return user # auth_user

    @classmethod
    def register_twitter_user(cls, user, key, secret):
        "Get or create specified Twitter User."
        user_id, user_data = (user.id, user)
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
        db.session.commit()
        return user # twitter_user

    @classmethod
    def register_news_reader(cls, auth_user, twitter_user):
        "Get or create Mixed News Reader (i.e. from aggregator)."
        reader = MixedReader.query.filter_by(
            twitter_user_id=twitter_user.user_id).first() # reader
        if not reader: # new
            reader = MixedReader(twitter_user_id=twitter_user.user_id)
            db.session.add(reader)
        else: # exists
            reader = db.session.merge(reader)
        reader.auth_user_id = auth_user.id # anyhow
        db.session.commit()
        return reader # mixed_reader

    
    @property
    def reader(self):
        return MixedReader.query.filter_by(auth_user_id=self.id).one()
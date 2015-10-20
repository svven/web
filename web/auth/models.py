"""
Auth models.
"""
from flask.ext.login import UserMixin

from .. import config, db
from ..news.models import WebReader
from database.models import AuthUser, TwitterUser, Token, Timeline

from aggregator.utils import munixtime

from tweepy import Twitter
CONSUMER_KEY, CONSUMER_SECRET = (
    config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)

class WebUser(AuthUser, UserMixin):
    "Web User."

    @classmethod
    def exists(cls, provider_name, user, key, secret):
        "Verify if user exists by specified provider."
        assert provider_name == 'twitter' # yet
        screen_name = user.screen_name
        return bool(WebUser.query.filter_by(screen_name=screen_name).count())

    @classmethod
    def create(cls, screen_name):
        "Create auth user by screen_name."
        user = WebUser(screen_name=screen_name)
        return WebUser.register_auth_user(user)

    @classmethod
    def authenticate(cls, provider_name, user, key, secret):
        "Authenticate based on provider user credentials."
        assert provider_name == 'twitter' # yet
        auth_user, created = WebUser.register_auth_user(user)
        twitter_user, _ = WebUser.register_twitter_user(user, key, secret)
        news_reader, _ = WebUser.register_news_reader(auth_user, twitter_user)
        return auth_user, created

    @classmethod
    def register_auth_user(cls, user):
        "Get or create specified Auth User."
        created = False
        screen_name, user_data = (user.screen_name, user)
        user = WebUser.query.filter_by(screen_name=screen_name).first()
        if not user: # new
            user = WebUser(user=user_data) # auth_user
            created = True
            db.session.add(user)
        else: # exists
            user.load(user_data) # update
            user = db.session.merge(user)
        db.session.commit()
        return user, created # auth_user

    @classmethod
    def register_twitter_user(cls, user, key, secret):
        "Get or create specified Twitter User."
        created = False
        user_id, user_data = (user.id, user)
        user = TwitterUser.query.filter_by(user_id=user_id).first() # twitter_user
        if not user: # new
            user = TwitterUser(user_data, key, secret)
            created = True
            db.session.add(user)
        else: # exists
            user.load(user_data) # update
            user = db.session.merge(user)
            if not user.token:
                user.token = Token(user_id=user_id, key=key, secret=secret)
            else: # update access token
                user.token.key = key
                user.token.secret = secret
            if not user.timelines:
                user.timelines.append(Timeline(user_id=user_id))
        db.session.commit()
        return user, created # twitter_user

    @classmethod
    def register_news_reader(cls, auth_user, twitter_user):
        "Get or create Mixed News Reader (i.e. from aggregator)."
        created = False
        reader = WebReader.query.filter_by(
            twitter_user_id=twitter_user.user_id).first() # reader
        if not reader: # new
            reader = WebReader(twitter_user_id=twitter_user.user_id)
            created = True
            db.session.add(reader)
        else: # exists
            reader = db.session.merge(reader)
        reader.auth_user_id = auth_user.id # anyhow
        db.session.commit()
        return reader, created # mixed_reader


    def __repr__(self):
        return '<User (%s): %s>' % (self.id, self.screen_name)

    @property
    def reader(self):
        # return WebReader.query.filter_by(auth_user_id=self.id).one()
        base_reader = super(WebUser, self).reader
        base_reader.__class__ = WebReader
        return base_reader # cached
    
    @property
    def registered_at_ux(self):
        return munixtime(self.registered_at)
    
    # Twitter properties
    @property
    def twitter_user(self):
        return self.reader.twitter_user
    
    @property
    def twitter(self):
        token = self.twitter_user.token
        access_token = { token.user_id: (token.key, token.secret) }
        return Twitter(CONSUMER_KEY, CONSUMER_SECRET, access_token)

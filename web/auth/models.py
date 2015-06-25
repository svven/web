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
    def exists(cls, provider_name, user, key, secret):
        "Verify if user exists by specified provider."
        assert provider_name == 'twitter' # yet
        screen_name = user.screen_name
        return bool(User.query.filter_by(screen_name=screen_name).count())

    @classmethod
    def authenticate(cls, provider_name, user, key, secret):
        "Authenticate based on provider user credentials."
        assert provider_name == 'twitter' # yet
        auth_user, created = User.register_auth_user(user)
        twitter_user, _ = User.register_twitter_user(user, key, secret)
        news_reader, _ = User.register_news_reader(auth_user, twitter_user)
        return auth_user, created

    @classmethod
    def register_auth_user(cls, user):
        "Get or create specified Svven Auth User."
        created = False
        screen_name, user_data = (user.screen_name, user)
        user = User.query.filter_by(screen_name=screen_name).first()
        if not user: # new
            user = User(user_data) # auth_user
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
            if not user.timeline:
                user.timeline = Timeline(user_id=user_id)
        db.session.commit()
        return user, created # twitter_user

    @classmethod
    def register_news_reader(cls, auth_user, twitter_user):
        "Get or create Mixed News Reader (i.e. from aggregator)."
        created = False
        reader = MixedReader.query.filter_by(
            twitter_user_id=twitter_user.user_id).first() # reader
        if not reader: # new
            reader = MixedReader(twitter_user_id=twitter_user.user_id)
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
        # return MixedReader.query.filter_by(auth_user_id=self.id).one()
        base_reader = super(User, self).reader
        base_reader.__class__ = MixedReader
        return base_reader # cached

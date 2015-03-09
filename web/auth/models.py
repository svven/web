"""
Auth models.
"""
from flask.ext.login import UserMixin

from .. import db
from database.auth.models import User as AuthUser
from database.twitter.models import User as TwitterUser

class User(AuthUser, UserMixin):
    "Svven user."

    @classmethod
    def authenticate(cls, provider_name, user, key, secret):
        "Authenticate based on provider user credentials."
        assert provider_name == 'twitter' # yet
        session = db.Session()
        user_id, user_data = (user.id, user)
        user = session.query(TwitterUser).\
            filter_by(user_id=user_id).first() # twitter_user
        if not user: # new
            user = TwitterUser(user_data, key, secret)
            session.add(user)
            session.commit() # atomic
        else: # exists
            user.load(user_data) # update
            user = session.merge(user) # just in case
            if not user.token:
                user.token = Token(user_id=user_id, key=key, secret=secret)
            else:
                user.token.key = key
                user.token.secret = secret
            if not user.timeline:
                user.timeline = Timeline(user_id=user_id)
        reader = session.query(Reader).\
            filter_by(twitter_user_id=user_id).first() # reader
        if not reader: # new
            reader = Reader(twitter_user_id=user_id)
            session.add(reader)
            session.commit() # atomic
        if not reader.auth_user: # new
            user = User(user_data) # auth_user
            session.add(user)
            reader.auth_user = user
        else: # exists
            user = session.query(User).get(reader.auth_user.id) # auth_user
            user.load(user_data) # update
            user = session.merge(user) # just in case
        session.commit()
        return user

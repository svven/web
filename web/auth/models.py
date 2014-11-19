"""
Models for user authentication.
"""
from ..extensions import db


class User(db.Model):
    """
    Authenticated user.
    """
    __tablename__ = 'auth_users'

    id = db.Column(db.BigInteger, primary_key=True)
    screen_name = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String)

    connection = db.relationship('Connection', backref='user', uselist=False)

    def __repr__(self):
        return '<User (%s): @%s>' % (self.id, self.screen_name)


class Connection(db.Model):
    """
    User connection.
    """
    __tablename__ = 'auth_connections'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, 
        db.ForeignKey('auth_users.id'), nullable=False, unique=True)
    tweeter_id = db.Column(db.BigInteger, 
        db.ForeignKey('twitter_tweeters.tweeter_id'), unique=True)
    # facebooker_id = db.Column(db.BigInteger,
    #     db.ForeignKey('facebook_facebookers.facebooker_id'), unique=True)

    tweeter = db.relationship('Tweeter')

    def __repr__(self):
        return '<Connection (%s): %s>' % (self.user_id, self.tweeter_id)


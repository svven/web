"""
Models for user authentication.
"""
from flask.ext.login import UserMixin

from ..extensions import db


class User(db.Model, UserMixin):
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

	# ================================================================
	# Class methods

	@classmethod
	def get_by_screen_name(cls, name):
		user = cls.query.filter(User.screen_name == name).first()

		if user:
			authenticated = True
		else:
			authenticated = False
		return user, authenticated


	@classmethod
	def authenticate(cls, login):
		user = cls.query.filter(db.or_(User.name == login, User.email == login)).first()

		if user:
			authenticated = True
		else:
			authenticated = False
		return user, authenticated

	@classmethod
	def search(cls, keywords):
		criteria = []
		for keyword in keywords.split():
			keyword = '%' + keyword + '%'
			criteria.append(db.or_(
				User.name.ilike(keyword),
				User.email.ilike(keyword),
			))
		q = reduce(db.and_, criteria)
		return cls.query.filter(q)


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

	tweeter = db.relationship('Tweeter')

	def __repr__(self):
		return '<Connection (%s): %s>' % (self.user_id, self.tweeter_id)


class Tweeter(db.Model):
	"""
	Twitter user that is tweeting links.
	"""
	__tablename__ = 'twitter_tweeters'

	id = db.Column(db.BigInteger, primary_key=True)
	tweeter_id = db.Column(db.BigInteger, nullable=False, unique=True)
	screen_name = db.Column(db.String, nullable=False, unique=True)
	name = db.Column(db.String)
	description = db.Column(db.String)
	profile_image_url = db.Column(db.String)
	protected = db.Column(db.Boolean)
	friends_count = db.Column(db.Integer)
	followers_count = db.Column(db.Integer)

	tweets = db.relationship('Tweet', backref='tweeter', lazy='dynamic')
	timeline = db.relationship('Timeline', backref='tweeter', uselist=False)
	token = db.relationship('Token', backref='tweeter', uselist=False)

	def __init__(self, user):
		"Param `user` is a Twitter API user."
		self.tweeter_id = user.id
		self.screen_name = user.screen_name
		self.name = user.name
		self.description = user.description
		self.profile_image_url = user.profile_image_url
		self.friends_count = user.friends_count
		self.followers_count = user.followers_count

	def __repr__(self):
		return '<Tweeter (%s): @%s>' % (self.tweeter_id, self.screen_name)


class Token(db.Model):
	"""
	Twitter API access token for user.
	"""
	__tablename__ = 'twitter_tokens'

	id = db.Column(db.BigInteger, primary_key=True)
	tweeter_id = db.Column(db.BigInteger,
	                       db.ForeignKey('twitter_tweeters.tweeter_id'), nullable=False, unique=True)
	key = db.Column(db.String, nullable=False)
	secret = db.Column(db.String, nullable=False)

	def __repr__(self):
		return '<Token (%s): %s>' % (self.tweeter_id, self.key.split('-')[1])


class Timeline(db.Model):
	"""
	Twitter timeline that is being polled.
	"""
	__tablename__ = 'twitter_timelines'

	METHODS = (USER_TIMELINE, HOME_TIMELINE) = ('user', 'home')
	DEFAULT_FREQUENCY = 15 * 60  # 15 mins
	MIN_FREQUENCY = 2 * 60  # 2 mins
	MAX_FREQUENCY = 2 * 24 * 60 * 60  # 2 days
	MAX_FAILURES = 5  # to keep enabled

	id = db.Column(db.BigInteger, primary_key=True)
	tweeter_id = db.Column(db.BigInteger,
	                       db.ForeignKey('twitter_tweeters.tweeter_id'), nullable=False, unique=True)
	method = db.Column(db.Enum(*METHODS, name='timeline_method'), nullable=False)
	since_id = db.Column(db.BigInteger)
	next_check = db.Column(db.DateTime(timezone=True), default=db.func.now())
	prev_check = db.Column(db.DateTime(timezone=True))
	frequency = db.Column(db.Integer, nullable=False, default=DEFAULT_FREQUENCY)
	failures = db.Column(db.SmallInteger, nullable=False, default=0)
	enabled = db.Column(db.Boolean, nullable=False, default=True)

	def __repr__(self):
		return '<Timeline (%s): %s>' % (self.tweeter_id, self.method.upper())


class Tweet(db.Model):
	"""
	Twitter status containing a link by tweeter.
	"""
	__tablename__ = 'twitter_tweets'

	id = db.Column(db.BigInteger, primary_key=True)
	status_id = db.Column(db.BigInteger, nullable=False, unique=True)
	tweeter_id = db.Column(db.BigInteger,
	                       db.ForeignKey('twitter_tweeters.tweeter_id'), nullable=False)
	source_url = db.Column(db.String, nullable=False)
	created_at = db.Column(db.DateTime(timezone=True))
	link_id = db.Column(db.String)
	# db.ForeignKey('reader_links.link_id')
	processed = db.Column(db.Boolean, nullable=False, default=False)

	def __init__(self, status):
		"Param `status` is a Twitter API status."
		self.status_id = status.id
		self.tweeter_id = status.user.id
		self.created_at = status.created_at

	def __repr__(self):
		return '<Tweet (%s): %s>' % (self.tweeter_id, self.source_url)



"""
Config settings for web app.
"""
import os

def from_object(updates):
    "Update same name (or prefixed) settings."
    import sys
    config = sys.modules[__name__]

    prefix = config.__name__.split('.')[0].upper()
    keys = [k for k in config.__dict__ if \
        k != from_object.__name__ and not k.startswith('_')]
    get_value = lambda c, k: hasattr(c, k) and getattr(c, k) or None
    for key in keys:
        prefix_key = '%s_%s' % (prefix, key)
        value = get_value(updates, prefix_key) or get_value(updates, key)
        if value: setattr(config, key, value)

DEBUG = True
# SERVER_NAME = 'dev.svven.com'
SECRET_KEY = '\xc6d\xd4\xbeg\x18V?\xe0\x81\xe5D\x95_\xca02B\x83\t\x07\xb1\x84\x91'

## SQLAlchemy
## http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html
SQLALCHEMY_ECHO = sqlalchemy_echo = True

DATABASE_HOST = os.environ.get('DATABASE_HOST', 'localhost')
SQLALCHEMY_DATABASE_URI = sqlalchemy_url = 'postgresql://svven@%s/svven' % DATABASE_HOST

## Twitter # @SvvenDotCom
TWITTER_CONSUMER_KEY = 'Jrp1bcXiSahhWAqn3VJb4fzsg'
TWITTER_CONSUMER_SECRET = '36xO8Y8YT7Y0hRHDwoULuTU2xyru6cPkCSrRxLoJAzZ3hmxhfS'

OAUTH_CREDENTIALS = {
    'twitter': {
        'key': TWITTER_CONSUMER_KEY,
        'secret': TWITTER_CONSUMER_SECRET
    }
}

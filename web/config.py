"""
Config settings for web app.
"""
import os, socket

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

DEBUG = False
# SERVER_NAME = 'svven.com'
SECRET_KEY = '\xc6d\xd4\xbeg\x18V?\xe0\x81\xe5D\x95_\xca02B\x83\t\x07\xb1\x84\x91'

## SQLAlchemy
## http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html
SQLALCHEMY_ECHO = sqlalchemy_echo = False

DATABASE_HOST = os.environ.get('DATABASE_HOST', 'localhost')
SQLALCHEMY_DATABASE_URI = sqlalchemy_url = 'postgresql://svven@%s/svven' % DATABASE_HOST

## Aggregator
AGGREGATOR_REDIS_HOST = os.environ.get('AGGREGATOR_REDIS_HOST', 'localhost')
AGGREGATOR_REDIS_PORT = 6379
AGGREGATOR_REDIS_DB = 1

AGGREGATOR_BASE_UXTIME = 1420070400 # datetime(2015, 1, 1, 0, 0) # 1

## RQ (Redis Queue)
RQ_REDIS_HOST = os.environ.get('RQ_REDIS_HOST', 'localhost')
RQ_REDIS_PORT = 6379
RQ_REDIS_DB = 0

## Twitter # @SvvenDotCom
TWITTER_CONSUMER_KEY = 'Jrp1bcXiSahhWAqn3VJb4fzsg'
TWITTER_CONSUMER_SECRET = '36xO8Y8YT7Y0hRHDwoULuTU2xyru6cPkCSrRxLoJAzZ3hmxhfS'

OAUTH_CREDENTIALS = {
    'twitter': {
        'key': TWITTER_CONSUMER_KEY,
        'secret': TWITTER_CONSUMER_SECRET
    }
}

## Summary
SUMMARY_USER_AGENT = 'Svven-Summarizer'
SUMMARY_ADBLOCK_EASYLIST_URL = 'easylist.txt' # offline
  # 'https://easylist-downloads.adblockplus.org/easylist.txt' #
SUMMARY_ADBLOCK_EXTRALIST_URL = 'extralist.txt' # offline
  # 'https://dl.dropboxusercontent.com/u/134594/svven/extralist.txt' #
SUMMARY_USEFUL_QUERY_KEYS = [
    'v', 's', 'id', 'story_fbid', 'set', 'q', 'cid', 'tbm', 'fbid', 'u', 'p', 
    'next', 'article_id', 'articleid', 'a', 'gid', 'mid', 'itemid', 'newsid', 
    'storyid', 'list', 'piano_t', 'piano_d', 'page', 'diff', 'editors', 
    'storyId', 'l', 'm', 'video', 'kanal', 'pid', 'sid', 'item', 'f', 't', 
    'forum_id', 'path', 'url',
]
# SUMMARY_PHANTOMJS_BIN = '/usr/local/bin/phantomjs'
# SUMMARY_PHANTOMJS_SITES = [
    # 'readwrite.com', 'html5-ninja.com', 'rally.org', 'blogs.ft.com', 
    # 'i100.independent.co.uk',  'www.behance.net', 'www.psmag.com', 'po.st',
# ]
SUMMARY_NONCANONIC_SITES = [
    'docquery.fec.gov', 'c2.com', 'www.lukew.com', 'cyberdust.com', 
    'forums.station.sony.com', 'www.ecommercebytes.com', 
    'www.residentadvisor.net', 'hire.jobvite.com', 'everydaycarry.com',
    'www.google.com',
]

# ## DebugToolbar
# DEBUG_TB_HOSTS = ('127.0.0.1', )

## Google Analytics
GOOGLE_ANALYTICS_ID = 'UA-60733932-1'

## Papertrail
HOSTNAME = socket.gethostname()
PAPERTRAIL_HOST = 'logs3.papertrailapp.com'
PAPERTRAIL_PORT = '33078'

## Logging
LOGGING = '''
version: 1
disable_existing_loggers: true
root:
    level: INFO
    propagate: true
loggers:
    web:
        handlers: [papertrail]
        level: INFO
    poller:
        handlers: [console]
        level: WARNING
    summary:
        handlers: [console]
        level: WARNING
    summarizer:
        handlers: [console]
        level: WARNING
handlers:
    console:
        level: DEBUG
        class: logging.StreamHandler
        formatter: console
    papertrail:
        level: INFO
        class: logging.handlers.SysLogHandler
        address: [{papertrail_host}, {papertrail_port}]
        formatter: papertrail
formatters:
    console:
        format: '%(name)s {hostname}.%(process)d %(levelname)s: %(message)s'
        datefmt: '%H:%M:%S'
    papertrail:
        format: '%(name)s {hostname}.%(process)d %(levelname)s: %(message)s'
        datefmt: '%H:%M:%S'
'''
LOGGING = LOGGING.format(hostname=HOSTNAME,
    papertrail_host=PAPERTRAIL_HOST, papertrail_port=PAPERTRAIL_PORT)
LOGGER_NAME = 'web'

"""
Web initialization.
"""
import config, database, aggregator

from flask_cache import Cache
from flask_sqlalchemy import SQLAlchemy

def init(config_updates=None):
    """
    Delayed init to allow config updates.
    Updates can be passed as param here or set onto `config` upfront.
    i.e. `config.SETTING = updates.PREFIX_SETTING or updates.SETTING`
    """
    if config_updates:
        config.from_object(config_updates)

    global db

    ## Database
    database.init(config)
    # db = database.db # just sqlalchemy
    db = SQLAlchemy() # flask_sqlalchemy

    ## Aggregator
    aggregator.init(config) # delayed init

    # ## Cache
    # cache = Cache()

"""
Web initialization.
"""
import config, database, aggregator

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

def init(config_updates=None):
    """
    Delayed init to allow config updates.
    Updates can be passed as param here or set onto `config` upfront.
    i.e. `config.SETTING = updates.PREFIX_SETTING or updates.SETTING`
    """
    if config_updates:
        config.from_object(config_updates)

    global bootstrap, db #, assets, cache

    ## Bootstrap
    bootstrap = Bootstrap()

    ## Database
    database.init(config)
    
    ## Plain SQLAlchemy
    # db = database.db

    ## Flask-SQLAlchemy
    db = SQLAlchemy()
    database.db = db

    ## Aggregator
    aggregator.init(config) # delayed init

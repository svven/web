"""
Web app factory.
"""
import config
from . import init

import os.path as path
import pkgutil, importlib
import logging, logging.config, yaml

from flask import Flask, Blueprint, render_template, current_app
# from flask_debugtoolbar import DebugToolbarExtension

__all__ = ['create_app'] # from app import *

def create_app(config_updates=None):
    "Create and configure the Flask app."
    
    init(config_updates) # delayed init
    from . import bootstrap, db

    package_name = __name__.split('.')[0]
    app = Flask(package_name)
    app.config.from_object(config)

    bootstrap.init_app(app)
    db.init_app(app)
    
    # toolbar = DebugToolbarExtension(app)
    app.logger # init
    logging.config.dictConfig(yaml.load(config.LOGGING))

    package_path = path.dirname(__file__)
    register_blueprints(app, package_name, package_path)

    if not app.debug:
        for e in [404, 500]:
            app.errorhandler(e)(handle_error)
    return app

def handle_error(e):
    current_app.logger.exception(e)
    code = hasattr(e, 'code') and e.code or 500
    return render_template('errors/%s.html' % code), code

def register_blueprints(app, package_name, package_path):
    """
    Register all Blueprint instances on the specified 
    Flask app found in all modules for the specified package.
    """
    rv = []
    for _, name, _ in pkgutil.iter_modules(path=[package_path]):
        m = importlib.import_module('%s.%s' % (package_name, name))
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
            rv.append(item)
    return rv

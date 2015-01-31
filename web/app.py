"""
Web app factory.
"""
import config
from . import init

import pkgutil, importlib
from flask import Flask, render_template

__all__ = ['create_app'] # from app import *

def create_app(config_updates=None):
    "Create and configure the Flask app."
    
    init(config_updates) # delayed init
    from . import db, assets #, mail, security

    name = __name__.split('.')[0]
    app = Flask(name)
    app.config.from_object(config)

    db.init_app(app)
    assets.init_app(app)
    # mail.init_app(app)
    # security.init_app(app)

    # register_blueprints(app, name, __path__)

    if not app.debug:
        for e in [403, 404, 500]:
            app.errorhandler(e)(handle_error)

    return app

def handle_error(e):
    return render_template('errors/%s.html' % e.code), e.code

# def register_blueprints(app, package_name, package_path):
#     """Register all Blueprint instances on the specified Flask application found
#     in all modules for the specified package.

#     :param app: the Flask application
#     :param package_name: the package name
#     :param package_path: the package path
#     """
#     rv = []
#     for _, name, _ in pkgutil.iter_modules(package_path):
#         m = importlib.import_module('%s.%s' % (package_name, name))
#         for item in dir(m):
#             item = getattr(m, item)
#             if isinstance(item, Blueprint):
#                 app.register_blueprint(item)
#             rv.append(item)
#     return rv

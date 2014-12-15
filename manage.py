# -*- coding: utf-8 -*-

from flask_script import Manager

from web.app import create_app
from web.extensions import db


app = create_app()
manager = Manager(app)
app.config['SENTRY_DSN'] = 'http://e2e8239ee0044f7cbe57c2055820cb10:4c55a700f0554e198ce4fcdcc01a66e9@localhost:9000/2'
# sentry = Sentry(app)


@manager.command
def run():
    """Run in local machine."""

    app.run()


@manager.command
def initdb():
    """Init/reset database."""

    db.drop_all()
    db.create_all()


manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()

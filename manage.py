# -*- coding: utf-8 -*-

from flask_script import Manager

from web.app import create_app
from web.extensions import db


app = create_app
manager = Manager(app)


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

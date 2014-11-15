# -*- coding: utf-8 -*-

from flask_script import Manager

from web import create_app
from web.extensions import db
from web.user import User, ADMIN, ACTIVE


app = create_app()
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

	admin = User(
		name=u'admin',
		email=u'admin@example.com',
		password=u'123456',
		role_code=ADMIN,
		status_code=ACTIVE)
	db.session.add(admin)
	db.session.commit()


manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
	manager.run()

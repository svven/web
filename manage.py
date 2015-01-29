"""
Web manager.
"""
from web.app import create_app
from web.extensions import db

from flask_script import Manager


app = create_app()
manager = Manager(app)

@manager.command
def run():
    "Run app."
    app.run()

# @manager.command
# def initdb():
#     "Init db."
#     # db.drop_all()
#     db.create_all()

manager.add_option('-c', '--config',
    dest="config", required=False, help="config file")

if __name__ == "__main__":
    manager.run()

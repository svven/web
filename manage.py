"""
Web manager.
"""
from web.app import *
app = create_app()

from manager import Manager
manager = Manager()


## Static content, temporarily
import os
@app.route('/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(path)

@manager.command
def run():
    "Run app in development mode."
    app.run(host='0.0.0.0', port=5000)

@manager.command
def invite(screen_name):
    "Allow specified user to sign up."
    with app.app_context():
        from web.auth.models import User
        user, created = User.create(screen_name)
        app.logger.info('%s invite: %s', 
            created and 'Created' or 'Redundant', screen_name)

if __name__ == '__main__':
    manager.main()

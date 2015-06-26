"""
Web manager.
"""
from web.app import *
app = create_app()

from manager import Manager
manager = Manager()


@manager.command
def run():
    app.run(host='0.0.0.0', port=5000)

@manager.command
def invite(screen_name):
    with app.app_context():
        from web.auth.models import User
        user, created = User.create(screen_name)
        print 'User %s %s.' % (screen_name, created and \
            'was created' or 'already exists')

## Static content, temporarily
import os
@app.route('/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(path)


if __name__ == '__main__':
    manager.main()

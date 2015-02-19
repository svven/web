"""
Web manager.
"""
from web.app import *
app = create_app()

from flask_script import Manager
manager = Manager(app)


@manager.command
def run():
    app.run(host='0.0.0.0', port=5000)


## Static content, temporarily
import os
@app.route('/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(path)


if __name__ == "__main__":
    manager.run()

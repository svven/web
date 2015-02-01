"""
Web manager.
"""
from web.app import create_app
app = create_app()

from flask_script import Manager
manager = Manager(app)

from web import db
from database.auth import *
from database.news import *
from database.twitter import *


@manager.command
def run():
    app.run()

@manager.command
def init_db():
    db.create_all()

import os
@app.route('/css/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('css', path))


@app.route('/')
def index():
    s = db.session

    # links = Link.query.count()
    # links = s.query(Link).count()

    ret = ''
    for mark_id, screen_name, created_at, url, title in \
        s.query(
            Mark.id, User.screen_name, Status.created_at, Link.url, Link.title).\
        join(Status, Link, Reader, User).\
        order_by(Status.created_at.desc()).limit(15):

        # select m.id, u.screen_name, s.created_at, l.url, l.title
        # from news_marks m
        # join twitter_statuses s on m.twitter_status_id = s.status_id
        # join news_links l on m.link_id = l.id
        # join news_readers r on m.reader_id = r.id
        # join twitter_users u on r.twitter_user_id = u.user_id
        # order by 2 desc
        # limit 100;

        ret += '<p><a href="{3}">{1}</a> <strong>@{0}</strong>: {2}</p>'.format(
            screen_name, created_at, title.encode('utf8'), url
        )
    return "<div style='font-family:Monaco'>%s</div>" % ret


if __name__ == "__main__":
    manager.run()

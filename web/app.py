from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, session, escape, request, redirect, url_for

from redsess import RedisSessionInterface


app = Flask(__name__)
app.session_interface = RedisSessionInterface()
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

#Make sure to remove this line before deploying to production.
app.debug = True

app.wsgi_app = ProxyFix(app.wsgi_app)


def sum_counter():
    try:
        session['counter'] += 1
    except KeyError:
        session['counter'] = 1


@app.route('/')
def index():
    if 'username' in session:
        sum_counter()
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
        '''


@app.route('/clear')
def clearsession():
    # Clear the session
    session.clear()
    # Redirect the user to the main page
    return redirect(url_for('index'))

 
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)




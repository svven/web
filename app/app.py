from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, url_for, request

app = Flask(__name__)

#Make sure to remove this line before deploying to production.
app.debug = True

app.wsgi_app = ProxyFix(app.wsgi_app)

@app.route('/')
def hello_world():
    return "Svven says Hello world!"
 
if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)

svven@vagrant-ubuntu-trusty-64:~/web$ 


# coding=utf-8
from bottle import Bottle, static_file
import beaker.middleware

import restriction
import vote
import user
import news
import config


app = Bottle()
app.mount('/restriction', restriction.app)
app.mount('/vote', vote.app)
app.mount('/user', user.app)
app.mount('/news', news.app)


@app.get('/')
def index():
    return static_file('index.html', root='../static/')


@app.get('/<path:path>')
def getfile(path):
    return static_file(path, root='../static/')

session_opts = {
    'session.type': 'ext:database',
    'session.url': config.db_url,
    'session.auto': True,
    'session.lock_dir': '/var/lock',
    'session.cookie_expires': False,
    'session.cookie_domain': config.cookie_domain,
    'session.secure': config.secure_cookies,
}

middleware_app = beaker.middleware.SessionMiddleware(app, session_opts)

# coding=utf-8
from bottle import Bottle, static_file
import restriction
import vote
import user
import news
import beaker.middleware
from model import dburl

app = Bottle()
app.mount('/rajoite', restriction.app)
app.mount('/kannatus', vote.app)
app.mount('/kayttaja', user.app)
app.mount('/tiedote', news.app)

@app.get('/')
def index():
	return static_file('index.html', root='../static/')

@app.get('/<path:path>')
def getfile(path):
	return static_file(path, root='../static/')

session_opts = {
	'session.type': 'ext:database',
	'session.url': dburl,
	'session.auto': True,
	'session.lock_dir': '/var/lock'
}

middleware_app = beaker.middleware.SessionMiddleware(app, session_opts)

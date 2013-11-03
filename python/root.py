# coding=utf-8
from bottle import Bottle, HTTPError, static_file, redirect, hook, request
import rajoite
import kannatus
import kayttaja
import beaker.middleware

app = Bottle()
app.mount('/rajoite', rajoite.app)
app.mount('/kannatus', kannatus.app)
app.mount('/kayttaja', kayttaja.app)

@app.get('/')
def index():
	return static_file('index.html', root='../static/')

@app.get('/<path:path>')
def getfile(path):
	return static_file(path, root='../static/')

session_opts = {
	'session.type': 'file',
	'session.data_dir': './session/',
	'session.auto': True
}

middleware_app = beaker.middleware.SessionMiddleware(app, session_opts)

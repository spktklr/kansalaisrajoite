# coding=utf-8
from bottle import Bottle, HTTPError, request
import model
from utils import session_user, jsonplugin

app = Bottle()
app.install(model.plugin)
app.install(jsonplugin)

@app.get('/')
def read_all(db):
	user = session_user(request, db)
	is_admin = user and user.admin
	
	items = db.query(model.News).order_by(model.News.id.desc())
	return { 'news': [ i.toDict(is_admin) for i in items ] }

@app.post('/')
def create(db):
	user = session_user(request, db)
	is_admin = user and user.admin
	
	if not user:
		return HTTPError(401, 'Unauthorized')
	
	if not is_admin:
		return HTTPError(403, 'Forbidden')
	
	item = model.News()
	
	item.title = request.forms.get('title')
	item.body = request.forms.get('body')
	item.user = user
	
	db.add(item)

@app.delete('/<id:int>')
def delete(db, id):
	user = session_user(request, db)
	is_admin = user and user.admin
	
	item = db.query(model.News).filter_by(id=id).first()
	
	if not item:
		return HTTPError(404, 'Not found')
	
	if not user:
		return HTTPError(401, 'Unauthorized')
	
	if not is_admin:
		return HTTPError(403, 'Forbidden')
	
	db.delete(item)

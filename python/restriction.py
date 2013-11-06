# coding=utf-8
from bottle import Bottle, HTTPError, request
import model
from utils import session_user, jsonplugin

app = Bottle()
app.install(model.plugin)
app.install(jsonplugin)

@app.get('/<id:int>')
def read_one(db, id):
	item = db.query(model.Restriction).filter_by(id=id).first()
	
	if item:
		return item.toDict(True)
	
	raise HTTPError(404)

@app.get('/')
def read_all(db):
	user = session_user(request, db)
	is_admin = user and user.admin
	
	items = db.query(model.Restriction).filter_by(approved=True)
	return { 'restrictions': [ i.toDict(is_admin) for i in items ] }

@app.get('/jono')
def read_queue(db):
	user = session_user(request, db)
	is_admin = user and user.admin
	
	if is_admin:
		items = db.query(model.Restriction).filter_by(approved=False)
		return { 'restrictions': [ i.toDict(is_admin) for i in items ] }
	else:
		return HTTPError(401, 'Unauthorized')

@app.post('/')
def create(db):
	user = session_user(request, db)
	
	if not user:
		return HTTPError(401, 'Unauthorized')
	
	item = model.Restriction()
	
	item.title = request.forms.get('title')
	item.contents = request.forms.get('contents')
	item.arguments = request.forms.get('arguments')
	item.user = user
	
	db.add(item)

@app.delete('/<id:int>')
def delete(db, id):
	user = session_user(request, db)
	is_admin = user and user.admin
	
	item = db.query(model.Restriction).filter_by(id=id).first()
	
	if not item:
		return HTTPError(404, 'Not found')
	
	if not user:
		return HTTPError(401, 'Unauthorized')
	
	if user != item.user and not is_admin:
		return HTTPError(403, 'Forbidden')
	
	db.delete(item)

@app.post('/<id:int>/vahvista')
def approve(db, id):
	user = session_user(request, db)
	is_admin = user and user.admin
	
	if is_admin:
		item = db.query(model.Restriction).filter_by(id=id).first()
		
		if not item:
			return HTTPError(404, 'Not found')
		
		item.approved = not item.approved
		item.approver = user
	else:
		return HTTPError(401, 'Unauthorized')

# coding=utf-8
from bottle import Bottle, HTTPError, request
import model
from utils import session_user, jsonplugin

app = Bottle()
app.install(model.plugin)
app.install(jsonplugin)

@app.get('/<id:int>')
def read_one(db, id):
	user = session_user(request, db)
	
	if not user:
		return HTTPError(401, 'Unauthorized')
	
	item = db.query(model.Restriction).filter_by(id=id).first()
	
	if not item:
		return HTTPError(404, 'Not found')
	
	return {'voted': user in item.voters}


@app.post('/<id:int>')
def create(db, id):
	user = session_user(request, db)
	
	if not user:
		return HTTPError(401, 'Unauthorized')
	
	item = db.query(model.Restriction).filter_by(id=id).first()
	
	if not item:
		return HTTPError(404, 'Not found')
	
	item.voters.append(user)

@app.delete('/<id:int>')
def delete(db, id):
	user = session_user(request, db)
	
	if not user:
		return HTTPError(401, 'Unauthorized')
	
	item = db.query(model.Restriction).filter_by(id=id).first()
	
	if not item:
		return HTTPError(404, 'Not found')
	
	item.voters.remove(user)

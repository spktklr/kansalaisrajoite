# coding=utf-8
from bottle import Bottle, HTTPError, request
import model
from utils import session_user

app = Bottle()
app.install(model.plugin)

@app.get('/<id:int>')
def read_one(db, id):
	user = session_user(request, db)
	
	if not user:
		return HTTPError(401, 'Unauthorized')
	
	item = db.query(model.Rajoite).filter_by(id=id).first()
	
	if not item:
		return HTTPError(404, 'Not found')
	
	if user in item.kannattajat:
		return {'kannatettu': True}
	else:
		return {'kannatettu': False}

@app.post('/<id:int>')
def create(db, id):
	user = session_user(request, db)
	
	if not user:
		return HTTPError(401, 'Unauthorized')
	
	item = db.query(model.Rajoite).filter_by(id=id).first()
	
	if not item:
		return HTTPError(404, 'Not found')
	
	item.kannattajat.append(user)

@app.delete('/<id:int>')
def delete(db, id):
	user = session_user(request, db)
	
	if not user:
		return HTTPError(401, 'Unauthorized')
	
	item = db.query(model.Rajoite).filter_by(id=id).first()
	
	if not item:
		return HTTPError(404, 'Not found')
	
	item.kannattajat.remove(user)

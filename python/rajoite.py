# coding=utf-8
from bottle import Bottle, HTTPError, request
import model
from utils import session_user, jsonplugin

app = Bottle()
app.install(model.plugin)
app.install(jsonplugin)

@app.get('/<id:int>')
def read_one(db, id):
	item = db.query(model.Rajoite).filter_by(id=id).first()
	
	if item:
		return item.toDict(True)
	
	raise HTTPError(404)

@app.get('/')
def read_all(db):
	user = session_user(request, db)
	is_admin = user and user.yllapitaja
	
	items = db.query(model.Rajoite).filter_by(vahvistettu=True)
	return { 'rajoitteet': [ i.toDict(is_admin) for i in items ] }

@app.get('/jono')
def read_waiting(db):
	user = session_user(request, db)
	is_admin = user and user.yllapitaja
	
	if is_admin:
		items = db.query(model.Rajoite).filter_by(vahvistettu=False)
		return { 'rajoitteet': [ i.toDict(is_admin) for i in items ] }
	else:
		return HTTPError(401, 'Unauthorized')

@app.post('/')
def create(db):
	user = session_user(request, db)
	
	if not user:
		return HTTPError(401, 'Unauthorized')
	
	rajoite = model.Rajoite()
	
	rajoite.otsikko = request.forms.get('otsikko')
	rajoite.sisalto = request.forms.get('sisalto')
	rajoite.perustelut = request.forms.get('perustelut')
	rajoite.kayttaja = user
	
	db.add(rajoite)

@app.delete('/<id:int>')
def delete(db, id):
	user = session_user(request, db)
	is_admin = user and user.yllapitaja
	
	item = db.query(model.Rajoite).filter_by(id=id).first()
	
	if not item:
		return HTTPError(404, 'Not found')
	
	if not user:
		return HTTPError(401, 'Unauthorized')
	
	if user != item.kayttaja and not is_admin:
		return HTTPError(403, 'Forbidden')
	
	db.delete(item)

@app.post('/<id:int>/vahvista')
def approve(db, id):
	user = session_user(request, db)
	is_admin = user and user.yllapitaja
	
	if is_admin:
		item = db.query(model.Rajoite).filter_by(id=id).first()
		
		if not item:
			return HTTPError(404, 'Not found')
		
		item.vahvistettu = not item.vahvistettu
		item.vahvistaja = user
	else:
		return HTTPError(401, 'Unauthorized')

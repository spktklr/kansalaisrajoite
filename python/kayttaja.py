# coding=utf-8
from bottle import Bottle, HTTPError, request
import model
import bcrypt
import datetime
from utils import session_user

app = Bottle()
app.install(model.plugin)

@app.post('/rekisteroidy')
def create(db):
	email = request.forms.get('email')
	nimi = request.forms.get('nimi')
	salasana = request.forms.get('salasana')
	
	if len(salasana) < 8:
		return HTTPError(400, 'Bad request')
	
	if db.query(model.Kayttaja).filter_by(email=email).first():
		return HTTPError(409, 'Conflict')
	
	kayttaja = model.Kayttaja()
	kayttaja.email = email
	kayttaja.nimi = nimi
	kayttaja.rekisteroitymisaika = datetime.datetime.now()
	kayttaja.salasana = bcrypt.hashpw(salasana, bcrypt.gensalt())
	db.add(kayttaja)

@app.post('/login')
def login(db):
	email = request.forms.get('email')
	salasana = request.forms.get('salasana')
	
	kayttaja = db.query(model.Kayttaja).filter_by(email=email).first()
	
	if kayttaja and bcrypt.hashpw(salasana, kayttaja.salasana.encode('utf-8')) == kayttaja.salasana:
		session = request.environ['beaker.session']
		session['user_id'] = kayttaja.id
		return kayttaja.toDict()
	else:
		return HTTPError(401)

@app.post('/logout')
def logout(db):
	user = session_user(request, db)
	
	if user:
		session.delete()
	else:
		return HTTPError(401, 'Unauthorized')

@app.get('/')
def read(db):
	user = session_user(request, db)
	
	if user:
		return user.toDict()
	else:
		return HTTPError(401, 'Unauthorized')

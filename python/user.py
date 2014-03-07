# coding=utf-8
from datetime import datetime, timedelta

from bottle import Bottle, HTTPError, request
from sqlalchemy.orm.exc import NoResultFound
import bcrypt

from utils import session_user, jsonplugin, gen_token, send_email
import model
import config


app = Bottle()
app.install(model.plugin)
app.install(jsonplugin)


@app.post('/rekisteroidy')
def register(db):
    email = request.forms.get('email')
    name = request.forms.get('name')
    password = request.forms.get('password')
    city = request.forms.get('city')

    if not password or len(password) < 8:
        return HTTPError(400, 'Bad request')

    if not email or len(email) == 0:
        return HTTPError(400, 'Bad request')

    if db.query(model.User).filter_by(email=email).first():
        return HTTPError(409, 'Conflict')

    user = model.User()
    user.email = email

    if name and len(name) > 0:
        user.name = name

    if city and len(city) > 0:
        user.city = city

    user.password = bcrypt.hashpw(password, bcrypt.gensalt())

    user.verified = False
    user.verification_token = gen_token()

    db.add(user)

    subject = config.verification_email_subject
    body = config.verification_email_body.format(
        email=user.email,
        site_name=config.site_name,
        site_url=config.site_url,
        token=user.verification_token
    )

    send_email(email, subject, body)


@app.post('/')
def modify(db):
    user = session_user(request, db)

    if not user:
        return HTTPError(401, 'Unauthorized')

    name = request.forms.get('name')
    password = request.forms.get('password')
    city = request.forms.get('city')

    if password:
        if len(password) < 8:
            return HTTPError(400, 'Bad request')
        else:
            user.password = bcrypt.hashpw(password, bcrypt.gensalt())

    if name:
        user.name = name
    else:
        user.name = None

    if city:
        user.city = city
    else:
        user.city = None

    return user.toDict(True)


@app.post('/vahvista')
def verify(db):
    email = request.forms.get('email')
    token = request.forms.get('token')

    if not email or not token:
        return HTTPError(400, 'Bad request')

    user = db.query(model.User).filter_by(email=email).first()

    if user and not user.verified and user.verification_token == token:
        user.verified = True
        user.verification_token = None

        session = request.environ['beaker.session']
        session['user_id'] = user.id

        return user.toDict(True)
    else:
        return HTTPError(401, 'Unauthorized')


@app.post('/nollaa-salasana-1')
def send_reset_email(db):
    email = request.forms.get('email')

    if not email:
        return HTTPError(400, 'Bad request')

    user = db.query(model.User).filter_by(email=email).first()

    if user:
        user.password_reset_initiated = datetime.now()
        user.password_reset_token = gen_token()

        subject = config.pw_reset_email_subject
        body = config.pw_reset_email_body.format(
            email=user.email,
            site_name=config.site_name,
            site_url=config.site_url,
            token=user.password_reset_token
        )

        send_email(email, subject, body)

    # to keep emails private we don't want to tell the user if the email exists


@app.post('/nollaa-salasana-2')
def reset_password(db):
    email = request.forms.get('email')
    token = request.forms.get('token')
    password = request.forms.get('password')

    if not email or not token or not password or len(password) < 8:
        return HTTPError(400, 'Bad request')

    user = db.query(model.User).filter_by(email=email).first()

    # pw reset token is valid for 1 hour
    if (user and user.password_reset_initiated and
            user.password_reset_initiated + timedelta(hours=1)
            >= datetime.now() and user.password_reset_token == token):
        user.password = bcrypt.hashpw(password, bcrypt.gensalt())

        user.password_reset_initiated = None
        user.password_reset_token = None

        # pw reset can also be used in activating the account
        user.verified = True
        user.verification_token = None
    else:
        return HTTPError(401, 'Unauthorized')


@app.post('/login')
def login(db):
    email = request.forms.get('email')
    password = request.forms.get('password')

    if not email or not password:
        return HTTPError(400, 'Bad request')

    user = db.query(model.User).filter_by(email=email).first()

    if user and not user.verified:
        return HTTPError(412, 'Precondition failed')
    if (user and user.verified and
            bcrypt.hashpw(password, user.password.encode('utf-8'))
            == user.password):
        session = request.environ['beaker.session']
        session['user_id'] = user.id
        return user.toDict(True)
    else:
        return HTTPError(401, 'Unauthorized')


@app.post('/logout')
def logout(db):
    session = request.environ.get('beaker.session')

    if session:
        session.delete()
    else:
        return HTTPError(401, 'Unauthorized')


@app.get('/')
def my_data(db):
    user = session_user(request, db)

    if user:
        return user.toDict(True)
    else:
        return {}


@app.get('/<id:int>')
def read_user(db, id):
    try:
        user = session_user(request, db)
        is_admin = user and user.admin

        if not is_admin:
            return HTTPError(401, 'Unauthorized')

        item = db.query(model.User).filter_by(id=id).one()
        return item.toDict(True)
    except NoResultFound:
        return HTTPError(404, 'Not found')

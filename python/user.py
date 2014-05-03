# coding=utf-8
import hmac
import json

from bottle import Bottle, HTTPError, request, template
from sqlalchemy.orm.exc import NoResultFound
import bcrypt

from utils import session_user, jsonplugin, gen_pw_reset_payload, send_email
import model
import config


app = Bottle()
app.install(model.plugin)
app.install(jsonplugin)


@app.post('/register')
def register(db):
    email = request.forms.get('email').strip()
    name = request.forms.get('name').strip()
    password = request.forms.get('password')
    city = request.forms.get('city').strip()

    if len(password) < 8:
        return HTTPError(400, 'Bad request')

    if not email:
        return HTTPError(400, 'Bad request')

    if db.query(model.User).filter_by(email=email).first():
        return HTTPError(409, 'Conflict')

    user = model.User()
    user.email = email

    if name:
        user.name = name

    if city:
        user.city = city

    user.password = bcrypt.hashpw(password, bcrypt.gensalt())

    db.add(user)

    # create hmac verification token
    token = hmac.new(config.site_secret, user.email).hexdigest()

    subject = config.verification_email_subject
    body = template(
        'mail_verification',
        email=user.email,
        site_name=config.site_name,
        site_url=config.site_url,
        token=token
    )

    send_email(email, subject, body)


@app.post('/')
def modify(db):
    user = session_user(request, db)

    if not user:
        return HTTPError(401, 'Unauthorized')

    name = request.forms.get('name').strip()
    password = request.forms.get('password')
    city = request.forms.get('city').strip()

    if len(password) < 8:
        return HTTPError(400, 'Bad request')
    elif password:
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


@app.post('/verify')
def verify(db):
    email = request.forms.get('email').strip()
    token = request.forms.get('token').strip()

    if not email or not token:
        return HTTPError(400, 'Bad request')

    if token != hmac.new(config.site_secret, email).hexdigest():
        return HTTPError(401, 'Unauthorized')

    user = db.query(model.User).filter_by(email=email).first()

    if user:
        user.verified = True

        session = request.environ['beaker.session']
        session['user_id'] = user.id

        return user.toDict(True)
    else:
        return HTTPError(404, 'Not found')


@app.post('/reset-password-1')
def send_reset_email(db):
    email = request.forms.get('email').strip()

    if not email:
        return HTTPError(400, 'Bad request')

    user = db.query(model.User).filter_by(email=email).first()

    if user:
        json_payload = json.dumps(gen_pw_reset_payload(user))

        token = hmac.new(config.site_secret, json_payload).hexdigest()

        subject = config.pw_reset_email_subject
        body = template(
            'mail_pw_reset',
            email=user.email,
            site_name=config.site_name,
            site_url=config.site_url,
            token=token
        )

        send_email(email, subject, body)

    # to keep emails private we don't want to tell the user if the email exists


@app.post('/reset-password-2')
def reset_password(db):
    email = request.forms.get('email').strip()
    token = request.forms.get('token').strip()
    password = request.forms.get('password')

    if not email or not token or not password or len(password) < 8:
        return HTTPError(400, 'Bad request')

    user = db.query(model.User).filter_by(email=email).first()

    if user:
        # validate hmac token
        json_payload = json.dumps(gen_pw_reset_payload(user))
        new_token = hmac.new(config.site_secret, json_payload).hexdigest()

        if token != new_token:
            return HTTPError(401, 'Unauthorized')

        # change password
        user.password = bcrypt.hashpw(password, bcrypt.gensalt())

        # pw reset can also be used in activating the account
        user.verified = True
    else:
        return HTTPError(401, 'Unauthorized')


@app.post('/login')
def login(db):
    email = request.forms.get('email').strip()
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

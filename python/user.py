# coding=utf-8
import hmac
import json

from bottle import Bottle, HTTPError, request, template
from sqlalchemy.orm.exc import NoResultFound
import bcrypt

from utils import jsonplugin, gen_pw_reset_payload, send_email
import auth
import model
import config
import utils


app = Bottle()
app.install(model.plugin)
app.install(jsonplugin)


@app.post('/register')
def register(db):
    try:
        email = request.forms.email.strip()

        if db.query(model.User).filter_by(email=email).first():
            return HTTPError(409, 'Conflict')

        user = model.User()
        user.email = email
        user.password = request.forms.password.strip()
        user.name = request.forms.name.strip()
        user.city = request.forms.city.strip()

        db.add(user)

        # create hmac verification token
        token = utils.sign_message(user.email)

        subject = config.verification_email_subject
        body = template(
            'mail_verification',
            email=user.email,
            site_name=config.site_name,
            site_url=config.site_url,
            token=token
        )

        send_email(email, subject, body)
    except AssertionError:
        return HTTPError(400, 'Bad request')


@app.post('/')
@auth.require_login
def modify(db, user):
    try:
        password = request.forms.get('password')

        if password:
            user.password = password

        user.name = request.forms.name.strip()
        user.city = request.forms.city.strip()

        return user.toDict(True)
    except AssertionError:
        return HTTPError(400, 'Bad request')


@app.post('/verify')
def verify(db):
    email = request.forms.email.strip()
    token = request.forms.token.strip()

    if not email or not token:
        return HTTPError(400, 'Bad request')

    expected_token = utils.sign_message(email)

    if not hmac.compare_digest(token, expected_token):
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
    email = request.forms.email.strip()

    if not email:
        return HTTPError(400, 'Bad request')

    user = db.query(model.User).filter_by(email=email).first()

    if user:
        json_payload = json.dumps(gen_pw_reset_payload(user))

        token = utils.sign_message(json_payload)

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
    try:
        email = request.forms.email.strip()
        token = request.forms.token.strip()

        if not email or not token:
            return HTTPError(400, 'Bad request')

        user = db.query(model.User).filter_by(email=email).first()

        if user:
            # validate hmac token
            json_payload = json.dumps(gen_pw_reset_payload(user))
            expected_token = utils.sign_message(json_payload)

            if not hmac.compare_digest(token, expected_token):
                return HTTPError(401, 'Unauthorized')

            # change password
            user.password = request.forms.password.strip()

            # pw reset can also be used in activating the account
            user.verified = True
        else:
            return HTTPError(401, 'Unauthorized')
    except AssertionError:
        return HTTPError(400, 'Bad request')


@app.post('/login')
def login(db):
    email = request.forms.email.strip()
    password = request.forms.password.strip()

    if not email or not password:
        return HTTPError(400, 'Bad request')

    user = db.query(model.User).filter_by(email=email).first()

    if user and not user.verified:
        return HTTPError(412, 'Precondition failed')
    if (user and user.verified and
            bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))):
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
@auth.optional_login
def my_data(db, user):
    if user:
        return user.toDict(True)
    else:
        return {}


@app.get('/<id:int>')
@auth.require_admin
def read_user(db, user, id):
    try:
        item = db.query(model.User).filter_by(id=id).one()
        return item.toDict(True)
    except NoResultFound:
        return HTTPError(404, 'Not found')

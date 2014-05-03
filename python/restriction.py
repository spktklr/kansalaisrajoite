# coding=utf-8
from bottle import Bottle, HTTPError, request
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload

import model
from utils import session_user, jsonplugin


app = Bottle()
app.install(model.plugin)
app.install(jsonplugin)


@app.get('/<id:int>')
def read_one(db, id):
    try:
        user = session_user(request, db)
        is_admin = user and user.admin

        item = db.query(model.Restriction) \
            .options(joinedload(model.Restriction.voters),
                     joinedload(model.Restriction.user),
                     joinedload(model.Restriction.approver)) \
            .filter_by(id=id).one()

        if item.state != 'APPROVED' and user != item.user and not is_admin:
            return HTTPError(403, 'Forbidden')

        return item.toDict(is_admin, user)
    except NoResultFound:
        return HTTPError(404, 'Not found')


@app.get('/')
def read_all(db):
    user = session_user(request, db)
    is_admin = user and user.admin

    if is_admin:
        items = db.query(model.Restriction) \
            .options(joinedload(model.Restriction.voters),
                     joinedload(model.Restriction.user),
                     joinedload(model.Restriction.approver))
    elif user:
        items = db.query(model.Restriction).filter(
            (model.Restriction.state == 'APPROVED') |
            (model.Restriction.user == user)) \
            .options(joinedload(model.Restriction.voters),
                     joinedload(model.Restriction.user))
    else:
        items = db.query(model.Restriction).filter(
            model.Restriction.state == 'APPROVED') \
            .options(joinedload(model.Restriction.voters))

    return {'restrictions': [i.toDict(is_admin, user) for i in items]}


@app.post('/')
def create(db):
    user = session_user(request, db)

    if not user:
        return HTTPError(401, 'Unauthorized')

    title = request.forms.get('title').strip()
    body = request.forms.get('body').strip()
    name = request.forms.get('name').strip()
    city = request.forms.get('city').strip()

    for field in [title, body, name, city]:
        if not field:
            return HTTPError(400, 'Bad request')

    item = model.Restriction()
    item.title = title
    item.body = body
    item.state = 'NEW'
    item.user = user
    item.user_name = name
    item.user_city = city
    item.voters.append(user)

    db.add(item)
    db.flush()

    return {'id': item.id, 'title': item.title}


@app.delete('/<id:int>')
def delete(db, id):
    try:
        user = session_user(request, db)
        is_admin = user and user.admin

        if not user:
            return HTTPError(401, 'Unauthorized')

        item = db.query(model.Restriction).filter_by(id=id).one()

        if user != item.user and not is_admin:
            return HTTPError(403, 'Forbidden')

        db.delete(item)
    except NoResultFound:
        return HTTPError(404, 'Not found')


@app.post('/<id:int>/approve')
def approve(db, id):
    try:
        user = session_user(request, db)
        is_admin = user and user.admin

        if not is_admin:
            return HTTPError(403, 'Forbidden')

        item = db.query(model.Restriction).filter_by(id=id).one()
        item.state = 'APPROVED'
        item.approver = user
    except NoResultFound:
        return HTTPError(404, 'Not found')


@app.post('/<id:int>/reject')
def reject(db, id):
    try:
        user = session_user(request, db)
        is_admin = user and user.admin

        if not is_admin:
            return HTTPError(403, 'Forbidden')

        item = db.query(model.Restriction).filter_by(id=id).one()
        item.state = 'REJECTED'
        item.approver = user
    except NoResultFound:
        return HTTPError(404, 'Not found')

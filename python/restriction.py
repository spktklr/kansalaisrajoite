# coding=utf-8
from bottle import Bottle, HTTPError, request
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload

import model
from utils import jsonplugin
import auth


app = Bottle()
app.install(model.plugin)
app.install(jsonplugin)


@app.get('/<id:int>')
@auth.optional_login
def read_one(db, user, id):
    is_admin = user and user.admin

    try:
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
@auth.optional_login
def read_all(db, user):
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
@auth.require_login
def create(db, user):
    try:
        item = model.Restriction()
        item.title = request.forms.title.strip()
        item.body = request.forms.body.strip()
        item.state = 'NEW'
        item.user = user
        item.user_name = request.forms.name.strip()
        item.user_city = request.forms.city.strip()
        item.voters.append(user)

        db.add(item)
        db.flush()

        return {'id': item.id, 'title': item.title}
    except AssertionError:
        return HTTPError(400, 'Bad request')


@app.delete('/<id:int>')
@auth.require_login
def delete(db, user, id):
    try:
        is_admin = user and user.admin

        item = db.query(model.Restriction).filter_by(id=id).one()

        if user != item.user and not is_admin:
            return HTTPError(403, 'Forbidden')

        db.delete(item)
    except NoResultFound:
        return HTTPError(404, 'Not found')


@app.post('/<id:int>/approve')
@auth.require_admin
def approve(db, user, id):
    try:
        item = db.query(model.Restriction).filter_by(id=id).one()
        item.state = 'APPROVED'
        item.approver = user
    except NoResultFound:
        return HTTPError(404, 'Not found')


@app.post('/<id:int>/reject')
@auth.require_admin
def reject(db, user, id):
    try:
        item = db.query(model.Restriction).filter_by(id=id).one()
        item.state = 'REJECTED'
        item.approver = user
    except NoResultFound:
        return HTTPError(404, 'Not found')

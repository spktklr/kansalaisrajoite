# coding=utf-8
from bottle import Bottle, HTTPError, request
from sqlalchemy.orm.exc import NoResultFound

import model
from utils import session_user, jsonplugin


app = Bottle()
app.install(model.plugin)
app.install(jsonplugin)


@app.get('/<id:int>')
def read_one(db, id):
    try:
        user = session_user(request, db)

        if not user:
            return HTTPError(401, 'Unauthorized')

        item = db.query(model.Restriction).filter_by(id=id).one()
        return {'voted': user in item.voters}
    except NoResultFound:
        return HTTPError(404, 'Not found')


@app.post('/<id:int>')
def create(db, id):
    try:
        user = session_user(request, db)

        if not user:
            return HTTPError(401, 'Unauthorized')

        item = db.query(model.Restriction).filter_by(id=id).one()
        item.voters.append(user)
    except NoResultFound:
        return HTTPError(404, 'Not found')


# Disabled
# @app.delete('/<id:int>')
def delete(db, id):
    try:
        user = session_user(request, db)

        if not user:
            return HTTPError(401, 'Unauthorized')

        item = db.query(model.Restriction).filter_by(id=id).one()
        item.voters.remove(user)
    except NoResultFound:
        return HTTPError(404, 'Not found')

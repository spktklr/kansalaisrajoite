# coding=utf-8
from bottle import Bottle, HTTPError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload

import model
from utils import jsonplugin
import auth


app = Bottle()
app.install(model.plugin)
app.install(jsonplugin)


@app.get('/<id:int>')
@auth.require_login
def read_one(db, user, id):
    try:
        item = db.query(model.Restriction) \
            .options(joinedload(model.Restriction.voters)) \
            .filter_by(id=id).one()
        return {'voted': user in item.voters}
    except NoResultFound:
        return HTTPError(404, 'Not found')


@app.post('/<id:int>')
@auth.require_login
def create(db, user, id):
    try:
        item = db.query(model.Restriction).filter_by(id=id).one()
        item.voters.append(user)
    except NoResultFound:
        return HTTPError(404, 'Not found')


# Disabled
# @app.delete('/<id:int>')
# @auth.require_login
def delete(db, user, id):
    try:
        item = db.query(model.Restriction).filter_by(id=id).one()
        item.voters.remove(user)
    except NoResultFound:
        return HTTPError(404, 'Not found')

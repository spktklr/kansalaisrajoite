# coding=utf-8
from bottle import Bottle, HTTPError, request
from sqlalchemy.orm.exc import NoResultFound

import model
from utils import jsonplugin
import auth


app = Bottle()
app.install(model.plugin)
app.install(jsonplugin)


@app.get('/')
@auth.optional_login
def read_all(db, user):
    is_admin = user and user.admin

    items = db.query(model.News).order_by(model.News.id.desc())
    return {'news': [i.toDict(is_admin) for i in items]}


@app.post('/')
@auth.require_admin
def create(db, user):
    item = model.News()

    item.title = request.forms.title.strip()
    item.body = request.forms.body.strip()
    item.user = user

    db.add(item)


@app.delete('/<id:int>')
@auth.require_admin
def delete(db, user, id):
    try:
        item = db.query(model.News).filter_by(id=id).one()
        db.delete(item)
    except NoResultFound:
        return HTTPError(404, 'Not found')

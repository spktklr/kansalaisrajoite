from bottle import Bottle, HTTPError, request

from sqlalchemy.orm.exc import NoResultFound

import model
from utils import jsonplugin
import auth


app = Bottle()
app.install(model.plugin)
app.install(jsonplugin)

@app.get('/<id:int>')
def read_one(db, id):
    try:
        items = db.query(model.Comment) \
            .filter_by(restriction_id=id).all()
        return {"comments" : [i.toDict() for i in items]}
    except NoResultFound:
        return HTTPError(404, 'Not found')

@app.post('/<id:int>')
@auth.require_login
def create(db, user, id):
    try:

        # comment = model.Comment
        #
        # comment.restriction_id = id
        # comment.user_id = user.id
        # comment.comment = request.forms.comment
        # #
        # # items = db.query(model.Comment).filter_by(restriction_id=id).all()
        # # print items
        #
        # item = db.query(model.Restriction).filter_by(id=id).one()
        # print item
        # print item.comments
        # item.comments.append(comment)
    except NoResultFound:
        return HTTPError(404, 'Not found')
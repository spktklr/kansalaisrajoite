from bottle import Bottle, HTTPError

from sqlalchemy.orm.exc import NoResultFound

import model
from utils import jsonplugin
import auth


app = Bottle()
app.install(model.plugin)
app.install(jsonplugin)

@app.post('/<id:int>')
@auth.require_login
def create(db, user, id):
    try:
        print user
        #item = db.query(model.Restriction).filter_by(id=id).one()
        #item.voters.append(user)
    except NoResultFound:
        return HTTPError(404, 'Not found')
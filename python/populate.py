# coding=utf-8
import json

from bottle import Bottle, HTTPError, request, template
from sqlalchemy.orm.exc import NoResultFound

from utils import jsonplugin, gen_pw_reset_payload, send_email
import model


app = Bottle()
app.install(model.plugin)
app.install(jsonplugin)


@app.get('/')
def populate(db):
    try:
        for i in range(10):
            user = model.User()
            user.email = 'user{}@example.com'.format(i)
            user.password = 'password'
            user.name = 'User{}'.format(i)
            user.city = 'City{}'.format(i)

            db.add(user)

            for j in range(10):
                item = model.Restriction()
                item.title = 'Rajoite {}'.format(j)
                item.body = 'Rajoite {}'.format(j)
                item.state = 'NEW'
                item.user = user
                item.user_name = user.name
                item.user_city = user.city
                item.voters.append(user)

                db.add(item)

        db.flush()
    except AssertionError:
        return HTTPError(400, 'Bad request')

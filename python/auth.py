# coding=utf-8
from bottle import HTTPError, request

import model


def optional_login(fn):
    def func(db, *args, **kwargs):
        session = request.environ.get('beaker.session')
        user_id = session.get('user_id')

        if not user_id:
            user = None
        else:
            user = db.query(model.User).filter_by(id=user_id).one()

        return fn(db, user, *args, **kwargs)

    return func


def require_login(fn):
    def func(db, *args, **kwargs):
        session = request.environ.get('beaker.session')
        user_id = session.get('user_id')

        if not user_id:
            return HTTPError(401, 'Unauthorized')

        user = db.query(model.User).filter_by(id=user_id).one()

        return fn(db, user, *args, **kwargs)

    return func


def require_admin(fn):
    def func(db, *args, **kwargs):
        session = request.environ.get('beaker.session')
        user_id = session.get('user_id')

        if not user_id:
            return HTTPError(401, 'Unauthorized')

        user = db.query(model.User).filter_by(id=user_id).one()
        is_admin = user and user.admin

        if not is_admin:
            return HTTPError(403, 'Forbidden')

        return fn(db, user, *args, **kwargs)

    return func

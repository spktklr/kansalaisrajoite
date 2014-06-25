# coding=utf-8
from bottle import Bottle, HTTPError, request, template
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload

import model
from utils import jsonplugin, slug, send_email
import auth
import config


app = Bottle()
app.install(model.plugin)
app.install(jsonplugin)


@app.get('/<id:int>')
@auth.optional_login
def read_one(db, user, id):
    is_admin = user and user.admin

    try:
        item = db.query(model.Restriction) \
            .options(joinedload(model.Restriction.voters)) \
            .filter_by(id=id).one()

        if item.state != 'APPROVED' and user != item.user and not is_admin:
            return HTTPError(403, 'Forbidden')

        result = item.toDict(True, user)

        if user:
            if user in item.voters:
                result['voted'] = True
            else:
                result['voted'] = False

        return result
    except NoResultFound:
        return HTTPError(404, 'Not found')


@app.get('/')
@auth.optional_login
def read_all(db, user):
    is_admin = user and user.admin

    if is_admin:
        items = db.query(model.Restriction)
    elif user:
        items = db.query(model.Restriction).filter(
            (model.Restriction.state == 'APPROVED') |
            (model.Restriction.user == user))
    else:
        items = db.query(model.Restriction).filter(model.Restriction.state == 'APPROVED')

    result = {'restrictions': [i.toDict(False, user) for i in items]}

    if user:
        votes = set()

        for voted in user.restrictions:
            votes.add(voted.id)

        for restriction in result['restrictions']:
            if restriction['id'] in votes:
                restriction['voted'] = True
            else:
                restriction['voted'] = False

    return result


@app.post('/')
@auth.require_login
def create(db, user):
    try:
        item = model.Restriction()
        item.title = request.forms.title.strip().capitalize()
        item.body = request.forms.body.strip()
        item.state = 'NEW'
        item.user = user
        item.user_name = request.forms.name.strip()
        item.user_city = request.forms.city.strip()
        item.voters.add(user)

        db.add(item)
        db.flush()

        if not user.admin:
            subject = config.restriction_created_email_subject
            body = template(
                'mail_restriction_created',
                site_name=config.site_name,
                site_url=config.site_url,
                id=item.id,
                slug=slug(item.title)
            )

            send_email(config.site_email, subject, body)

        return {'id': item.id, 'slug': slug(item.title)}
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
        db.flush()

        # email user the restriction was approved
        subject = config.restriction_approved_email_subject
        body = template(
            'mail_restriction_approved',
            site_name=config.site_name,
            site_url=config.site_url,
            id=item.id,
            slug=slug(item.title)
        )

        send_email(item.user.email, subject, body)
    except NoResultFound:
        return HTTPError(404, 'Not found')


@app.post('/<id:int>/reject')
@auth.require_admin
def reject(db, user, id):
    try:
        item = db.query(model.Restriction).filter_by(id=id).one()
        item.state = 'REJECTED'
        item.approver = user
        db.flush()

        # email user the restriction was rejected
        reason = request.forms.reason.strip()

        if reason:
            tpl = 'mail_restriction_rejected_reason'
        else:
            tpl = 'mail_restriction_rejected'

        subject = config.restriction_rejected_email_subject
        body = template(
            tpl,
            site_name=config.site_name,
            site_url=config.site_url,
            id=item.id,
            slug=slug(item.title),
            reason=reason
        )

        send_email(item.user.email, subject, body)
    except NoResultFound:
        return HTTPError(404, 'Not found')

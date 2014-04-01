# coding=utf-8
import json
import datetime
import smtplib
from email.mime.text import MIMEText

from bottle import JSONPlugin

import config
import model


def session_user(request, db):
    session = request.environ.get('beaker.session')
    if not session:
        print 'beaker.session not available'
        return None

    user_id = session.get('user_id')

    if not user_id:
        return None

    return db.query(model.User).filter_by(id=user_id).first()


def send_email(address, subject, body):
    message = MIMEText(body.encode('ISO-8859-1'))
    message['Subject'] = subject
    message['From'] = '%s <%s>' % (config.site_name, config.site_email)
    message['To'] = address

    smtp = smtplib.SMTP('localhost')
    smtp.sendmail(config.site_email, [address], message.as_string())


def gen_pw_reset_payload(user):
    # bundle old pw into hmac code to make this reset valid only
    # for the current pw
    return {
        'email': user.email,
        'password': user.password
    }


class JsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(obj.strftime('%s'))
        if isinstance(obj, datetime.date):
            return int(obj.strftime('%s'))
        return json.JSONEncoder.default(self, obj)

jsonplugin = JSONPlugin(json_dumps=lambda s: json.dumps(s, cls=JsonEncoder))

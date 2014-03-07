# coding=utf-8
import json
import datetime
import random
import string
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


def gen_token():
    charset = string.ascii_letters + string.digits
    return ''.join(random.choice(charset) for x in range(32))


def send_email(address, subject, body):
    message = MIMEText(body)
    message['Subject'] = subject
    message['From'] = '%s <%s>' % (config.site_name, config.site_email)
    message['To'] = address

    smtp = smtplib.SMTP('localhost')
    smtp.sendmail(config.site_email, [address], message.as_string())


class JsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(obj.strftime('%s'))
        if isinstance(obj, datetime.date):
            return int(obj.strftime('%s'))
        return json.JSONEncoder.default(self, obj)

jsonplugin = JSONPlugin(json_dumps=lambda s: json.dumps(s, cls=JsonEncoder))

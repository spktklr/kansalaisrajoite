# coding=utf-8
import hmac
import json
import datetime
import smtplib
from email.message import EmailMessage

from bottle import JSONPlugin
from slugify import slugify

import config

def send_email(address, subject, body):
    message = EmailMessage()
    message['Subject'] = subject
    message['From'] = '%s <%s>' % (config.site_name, config.site_email)
    message['To'] = address
    message.set_content(body)

    if config.DEV:
        print('sending email:')
        print(body)

    with smtplib.SMTP(config.smtp_host) as s:
        s.send_message(message)


def gen_pw_reset_payload(user):
    # bundle old pw into hmac code to make this reset valid only
    # for the current pw
    return {
        'email': user.email,
        'password': user.password
    }


def slug(s):
    return slugify(s, to_lower=True, max_length=100)


def sign_message(msg):
    key = bytes(config.site_secret, 'utf-8')
    data = bytes(msg, 'utf-8')

    return hmac.new(key, data).hexdigest()


class JsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(obj.strftime('%s'))
        if isinstance(obj, datetime.date):
            return int(obj.strftime('%s'))
        return json.JSONEncoder.default(self, obj)

jsonplugin = JSONPlugin(json_dumps=lambda s: json.dumps(s, cls=JsonEncoder))

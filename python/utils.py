# coding=utf-8
import json
import datetime
import smtplib
from email.mime.text import MIMEText

from bottle import JSONPlugin
from slugify import slugify

import config


def send_email(address, subject, body):
    if not config.EMAIL_ENABLED:
        return

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


def slug(s):
    return slugify(s, to_lower=True, max_length=100)


class JsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(obj.strftime('%s'))
        if isinstance(obj, datetime.date):
            return int(obj.strftime('%s'))
        return json.JSONEncoder.default(self, obj)

jsonplugin = JSONPlugin(json_dumps=lambda s: json.dumps(s, cls=JsonEncoder))

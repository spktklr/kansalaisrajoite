# coding=utf-8
import os

DEV = os.environ['DEVELOPMENT'] == 'true'
PROD = not DEV

protocol = os.environ['PROTOCOL']
domain = os.environ['DOMAIN']
db_url = os.environ['DB_URL']
smtp_host = os.environ['SMTP_HOST']

site_url = '{}://{}'.format(protocol, domain)
site_name = 'Kansalaisrajoite.fi'
site_email = 'yllapito@kansalaisrajoite.fi'

site_secret = os.environ['SITE_SECRET']

assert site_secret, 'SITE_SECRET is not set'

if PROD:
    cookie_domain = '.' + domain
    secure_cookies = True
else:
    cookie_domain = None
    secure_cookies = False

verification_email_subject = 'Rekisteröityminen'
pw_reset_email_subject = 'Salasanan palautus'
restriction_created_email_subject = 'Uusi rajoite luotu'
restriction_approved_email_subject = 'Rajoite hyväksytty'
restriction_rejected_email_subject = 'Rajoite hylätty'

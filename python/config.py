# coding=utf-8

site_url = 'https://kansalaisrajoite.fi'
site_name = 'Kansalaisrajoite.fi'
site_email = 'yllapito@kansalaisrajoite.fi'

db_url = 'postgresql+psycopg2:///kansalaisrajoite'

verification_email_subject = 'Rekisteröityminen'
verification_email_body = """Hei!

Rekisteröidyit {site_name}-palveluun käyttäen sähköpostiosoitetta {email}.
Vahvista rekisteröitymisesi klikkaamalla alla olevaa linkkiä:

{site_url}/#/vahvista/{email}/{token}


Terveisin,

{site_name} ylläpito"""

pw_reset_email_subject = 'Salasanan palautus'
pw_reset_email_body = """Hei!

Pyysit salasanasi palauttamista {site_name}-palvelussa. Jos et lähettänyt
pyyntöä voit ohittaa tämän viestin. Muussa tapauksessa vahvista salasanan
palautus klikkaamalla alla olevaa linkkiä:

{site_url}/#/uusi-salasana/{email}/{token}

Linkki on voimassa tunnin ajan.


Terveisin,

{site_name} ylläpito"""

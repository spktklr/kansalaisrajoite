# Kansalaisrajoite.fi

Mitä kieltäisimme seuraavaksi?

# Kehittäminen

Jos käytät vagranttia serverikoneena:

~~~bash
$ git clone https://github.com/spktklr/kansalaisrajoite
$ cp -R kansalaisrajoite/vagrant/* .
$ vagrant up \[port_guest\] \[port_host\]
$ vagrant ssh
    $ cd /vagrant/kansalaisrajoite/python
    $ python main.py --host "0.0.0.0" --debug [--port <port_guest>]


# To do

- Identiteetinhallinta
- SoMe-jakonapit ja toiminnallisuus
- Tietokanta ym.
- Tee kansalaisrajoite
- Ohjeet
- Tiedotteet
- Ota yhteyttä
- Henkilörekisteriseloste
- Henkilösuoja ja tietoturva
- På svenska & In English kevyet infosivut
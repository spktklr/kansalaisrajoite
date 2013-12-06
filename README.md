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
~~~

# TO DO
# toiminnallisuuksia
- SoMe-jakonapit yksittäisille rajoitteille
- Kansalaisrajoitteen submit, kierrättäminen tarkastuksessa ja show
- Rajoitteiden lajittelu ja sivutus
- Ota yhteyttä contactform

# tekstiä
- FB-sivu
- Tiedotteet
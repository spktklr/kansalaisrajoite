# Kansalaisrajoite.fi

Mitä kieltäisimme seuraavaksi?

## Dockerin käyttö

### Devaus

```
$ ENV=dev make build
$ ENV=dev make up
```

### Tuotanto

```
$ echo "SITE_SECRET=supersalainensalasana" > .env
$ ENV=prod make build
$ ENV=prod make up
```

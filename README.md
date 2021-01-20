# Virtual Office Radio

Listen to and control the office radio in the Workadventure instance

## API
```

GET /stream/<id> -> gibt die radio website für den stream zurück

GET /stream/<id>/url -> 307 redirect zu aktueller stream-url

GET /stream/<id>/status
GET /stream/<id>/json -> JSON object of stream status
GET /stream/<id>/json

POST /stream/<id>/play/<radio> , -> setzt den stream auf die url des vordefinierten stream namens (für die auswahl des streams beim radio )a
POST /stream/<id>/volume/<vol> -> setzt das volume des streams auf <vol> (0-100)

POST /stream/<id>/off
POST /stream/<id>/stop -> macht das radio aus

POST /stream/<id>/url , data: { "url": stream-url } -> setzt den stream auf url (expert mode)

GET / -> gibt die website mit der übersicht aller streams
GET /streams/json -> gibt alle streams mit status aus
GET /radios/json -> gibt alle verfügbaren konfigurierten Radios aus
```

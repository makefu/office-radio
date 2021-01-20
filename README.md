# Virtual Office Radio

Listen to and control the office radio in the Workadventure instance

## API
```
GET /streams/<id>/url -> 307 redirect zu aktueller stream-url
POST /streams/<id>/url , data: { "url": stream-url, "name": stream-name} -> setzt den stream auf url (expert mode)
POST /streams/<id>/name , data: { "name": stream-name } -> setzt den stream auf url des vordefinierten stream names (für die auswahl des streams beim radio )
POST /streams/<id>/off -> macht das radio aus
GET / -> gibt die website mit der übersicht aller streams
GET /streams/<id> -> gibt die radio website für den stream zurück
GET /streams/<id>/json -> gibt { "name": <stream-name>, "url": <stream-url>, "id": <id> }
```

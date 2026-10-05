# .data — dati persistenti dei servizi Docker

I container girano in Docker, ma i loro dati vivono qui sull'host, così
sopravvivono a `docker compose down`, ai rebuild e agli aggiornamenti delle
immagini. Le sottocartelle vengono create da Docker al primo avvio.

| Cartella | Servizio | Contenuto |
| --- | --- | --- |
| `postgres/` | postgres | cluster PostgreSQL (database app + database SonarQube) |
| `maildev/` | maildev | email catturate in sviluppo |
| `storage/` | app | file caricati dagli utenti in sviluppo (`STORAGE_DIR=/storage`) |
| `sonarqube/data`, `extensions`, `logs` | sonarqube | indici, plugin e log di SonarQube |

Regole:

- Il contenuto è escluso da Git (tranne questo file).
- **Sono dati da preservare**: cancellare una cartella non è una procedura di
  reset. Per ripartire da zero su un servizio, fermalo e fai prima un backup.
- I test non usano questa cartella: i loro database sono in RAM e spariscono
  a fine esecuzione.
- `postgres/` deve essere vuota alla prima inizializzazione: non aggiungere file.
- Gli script in `.docker/postgres/init/` girano solo quando `postgres/` è vuota.

Backup rapido del database dell'applicazione:

```sh
docker compose --env-file .env -f .docker/compose.app.yml exec -T postgres \
  sh -c 'pg_dump -U "$POSTGRES_USER" -Fc "$POSTGRES_DB"' > backup_$(date +%F).dump
```

Su Linux, se SonarQube non riesce a scrivere, assegna le cartelle
`sonarqube/*` all'utente 1000 (`sudo chown -R 1000:1000 .data/sonarqube`).

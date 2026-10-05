#!/bin/sh
# Eseguito solo alla prima inizializzazione di .data/postgres: crea utente e
# database di SonarQube accanto a quello dell'applicazione.
set -eu
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<SQL
CREATE USER "${SONAR_DB_USER}" WITH PASSWORD '${SONAR_DB_PASSWORD}';
CREATE DATABASE "${SONAR_DB}" OWNER "${SONAR_DB_USER}";
SQL

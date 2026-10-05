#!/bin/sh
# crond di busybox non passa le variabili d'ambiente ai job: le salviamo in un
# file letto da run-job. Il crontab viene copiato da /crontab (bind mount) così
# si modifica senza ricostruire l'immagine (basta riavviare il servizio).
set -eu
{
  echo "APP_INTERNAL_URL='${APP_INTERNAL_URL:-http://app:3000}'"
  echo "CRON_SECRET='${CRON_SECRET:-}'"
} > /etc/cron.env
chmod 600 /etc/cron.env
cp /crontab/crontab /etc/crontabs/root
echo "[cron] crontab caricato:"
grep -v '^\s*#' /etc/crontabs/root | grep -v '^\s*$' || echo "[cron] (nessun job attivo)"
exec crond -f -l 6 -c /etc/crontabs

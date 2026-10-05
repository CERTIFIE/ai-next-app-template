#!/bin/sh
# Uso: run-job <nome-job>  ->  GET $APP_INTERNAL_URL/api/cron/<nome-job>
set -eu
. /etc/cron.env
job="$1"
echo "[cron] $(date -u +%FT%TZ) avvio $job"
curl --fail --silent --show-error --max-time 300 \
  -H "Authorization: Bearer ${CRON_SECRET}" \
  "${APP_INTERNAL_URL}/api/cron/${job}" \
  && echo "[cron] $job completato" \
  || echo "[cron] $job FALLITO"

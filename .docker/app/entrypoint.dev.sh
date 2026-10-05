#!/bin/sh
# Entrypoint di sviluppo e test: installa le dipendenze nel volume
# /app/node_modules (binari Linux, mai quelli dell'host) solo quando
# package.json o il lockfile cambiano, poi esegue il comando richiesto.
set -eu
cd /app

if [ ! -f package.json ]; then
  echo "[entrypoint] package.json non trovato: lo scheletro non è ancora stato creato."
  echo "[entrypoint] Crea il progetto dentro il container, ad esempio:"
  echo "    docker compose --env-file .env -f .docker/compose.app.yml exec app sh"
  echo "    npx create-next-app@latest /tmp/scaffold ... e copia i file in /app"
  if [ "${WAIT_FOR_SCAFFOLD:-true}" = "true" ]; then
    exec sleep infinity
  fi
  exit 1
fi

if [ -f package-lock.json ]; then
  current_hash=$(cat package.json package-lock.json | sha256sum | cut -d' ' -f1)
  install_cmd="npm ci"
else
  current_hash=$(sha256sum package.json | cut -d' ' -f1)
  install_cmd="npm install"
fi

stamp=node_modules/.install-hash
if [ ! -f "$stamp" ] || [ "$(cat "$stamp")" != "$current_hash" ]; then
  echo "[entrypoint] Dipendenze cambiate: eseguo $install_cmd"
  $install_cmd
  echo "$current_hash" > "$stamp"
fi

exec "$@"

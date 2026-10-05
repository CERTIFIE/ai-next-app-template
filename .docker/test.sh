#!/usr/bin/env sh
# Esegue le suite di test in un ambiente Docker isolato e lo elimina alla fine.
#
# Uso:  .docker/test.sh [unit|integration|e2e|coverage|all] [argomenti per il runner]
#   unit         test unitari (nessun servizio esterno)
#   integration  test di integrazione su PostgreSQL e MailDev di prova
#   e2e          build di produzione + Playwright (profilo e2e)
#   coverage     unit + integration con copertura in reports/sonar/ (per SonarQube)
#   all          unit + integration (default)
#
# Ogni esecuzione ha un TEST_RUN_ID univoco: più agenti o worktree possono
# lanciare i test in parallelo senza condividere database, volumi o porte.
# La pulizia elimina solo le risorse del progetto Compose di questa esecuzione.
set -eu

SUITE="${1:-all}"
[ $# -gt 0 ] && shift
export TEST_ARGS="$*"

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="$ROOT/.env"
[ -f "$ENV_FILE" ] || ENV_FILE="$ROOT/.env.example"

if [ -z "${APP_NAME:-}" ]; then
  APP_NAME="$(grep -E '^APP_NAME=' "$ENV_FILE" | head -n1 | cut -d= -f2- | sed 's/[[:space:]]*#.*$//' | tr -d '"'"'"' ')"
fi
export APP_NAME="${APP_NAME:-app}"

if [ -z "${TEST_RUN_ID:-}" ]; then
  TEST_RUN_ID="$(date +%Y%m%d%H%M%S)_$(od -An -N3 -tx1 /dev/urandom | tr -d ' \n')"
fi
export TEST_RUN_ID

compose() {
  docker compose --env-file "$ENV_FILE" -f "$ROOT/.docker/compose.test.yml" --profile e2e "$@"
}

cleanup() {
  compose down --volumes --remove-orphans >/dev/null 2>&1 || true
}
trap cleanup EXIT
trap 'exit 130' INT TERM

# Cache npm condivisa tra le esecuzioni: esterna, quindi `down --volumes` non la tocca.
docker volume create "${APP_NAME}_npm_cache" >/dev/null

echo "[test] APP_NAME=$APP_NAME TEST_RUN_ID=$TEST_RUN_ID suite=$SUITE"

case "$SUITE" in
  unit)        compose run --rm unit ;;
  integration) compose run --rm integration ;;
  e2e)         compose run --rm e2e ;;
  all)         compose run --rm unit && compose run --rm integration ;;
  coverage)
    export TEST_REPORTS_NAME=sonar
    compose run --rm coverage
    ;;
  *) echo "Suite sconosciuta: $SUITE" >&2; exit 2 ;;
esac

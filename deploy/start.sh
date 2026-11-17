#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
: "${STORE_HOST:?Set the staging hostname}" "${ADMIN_EMAIL:?Set the owner email}"
if [[ ! -f .env ]]; then
  (umask 077; set -C; printf 'DB_PASSWORD=%s\n' "$(openssl rand -hex 32)" > .env)
fi
docker compose up -d db wordpress
cli() { docker compose run --rm -T cli "$@"; }
for attempt in {1..30}; do
  if cli core version >/dev/null 2>&1; then break; fi
  sleep 2
done
if ! cli core is-installed; then
  password="$(openssl rand -hex 24)"
  printf '%s\n' "$password" | cli core install --url="https://$STORE_HOST" --title=DY-AS --admin_user=dyas-owner --admin_email="$ADMIN_EMAIL" --prompt=admin_password
  printf 'Parola inițială DY-AS (salveaz-o acum): %s\n' "$password"
fi
docker compose run --rm -T --entrypoint bash cli /project/configure.sh
docker compose up -d web

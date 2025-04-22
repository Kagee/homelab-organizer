#! /bin/bash
cd "$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd .. # move to base dir
[[ "$1" = "debug-mount" ]] && figlet DEBUG-RUN && exec podman run \
  --init \
  --rm \
  --name hlo-debug \
  --env HLO_SECRET_KEY=secret \
  --env HLO_CSRF_TRUSTED_ORIGINS='https://*' \
  --env HLO_REMOTE_USER_HEADER=REMOTE_USER \
  --env HLO_DEBUG=true \
  --env HLO_REMOTE_USER_HEADER=Cf-Access-Authenticated-User-Email \
  --env APP_SUPERUSER_EMAIL=hildenae@gmail.com \
  --publish 127.0.0.1:8005:8000 \
  --volume "$PWD/docker/docker-entrypoint.sh:/custom-entrypoint.sh" \
  --volume "$PWD/hlo/:/app/hlo/" \
  localhost/hlo-debug

[[ "$1" = "debug" ]] && figlet DEBUG-RUN && exec podman run \
  --init \
  --rm \
  --name hlo-debug \
  --env HLO_SECRET_KEY=secret \
  --env HLO_CSRF_TRUSTED_ORIGINS='https://*' \
  --env HLO_REMOTE_USER_HEADER=REMOTE_USER \
  --env HLO_DEBUG=true \
  --env HLO_REMOTE_USER_HEADER=Cf-Access-Authenticated-User-Email \
  --env APP_SUPERUSER_EMAIL=hildenae@gmail.com \
  --publish 127.0.0.1:8005:8000 \
  localhost/hlo-debug


# ENV HLO_STATIC_ROOT=/app/static_root
# ENV HLO_MEDIA_ROOT=/app/media_root
# ENV HLO_SQLITE3_FILE=/app/db/hlo.sqlite3
# ENV HLO_WHOOSH_INDEX=/app/whoosh_index

figlet PROD-RUN && sudo podman run \
  --init \
  --rm \
  --name hlo \
  --env-file=./.env-prod \
  --env HLO_DEBUG=false \
  --env HLO_SQLITE3_FILE=/app/db/hlo.sqlite3 \
  --env HLO_STATIC_ROOT=/app/static_root \
  --env HLO_MEDIA_ROOT=/app/media_root \
  --env HLO_WHOOSH_INDEX=/app/whoosh_index \
  --volume /tank/data/hlo/static-test/:/app/static_root/ \
  --volume /tank/data/hlo/media-test/:/app/media_root/ \
  --volume /tank/data/hlo/db-test/:/app/db/ \
  --volume /tank/data/hlo/whoosh-test/:/app/whoosh_index/ \
  --publish 127.0.0.1:8000:8000 \
  localhost/hlo:prod

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

figlet PROD-RUN && podman run \
  --init \
  --rm \
  --name hlo \
  --env HLO_SECRET_KEY=secret \
  --env HLO_CSRF_TRUSTED_ORIGINS='https://*' \
  --env HLO_REMOTE_USER_HEADER=REMOTE_USER \
  --env HLO_DEBUG=false \
  --env HLO_REMOTE_USER_HEADER=Cf-Access-Authenticated-User-Email \
  --publish 127.0.0.1:8005:8000 \
  localhost/hlo

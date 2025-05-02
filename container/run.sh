#! /bin/bash
cd "$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )" || exit
cd .. # move to base dir

[[ "$1" = "mount-tmp" ]] && figlet DEV-MOUNT-TEMP && exec podman run \
  --init \
  --rm \
  --name hlo-dev \
  --env-file ./.env-dev \
  --publish 127.0.0.1:8005:8000 \
  --volume "$PWD/container/entrypoint.sh:/custom-entrypoint.sh" \
  --volume "$PWD/hlo/:/app/hlo/" \
  --volume "$PWD/static/:/app/static/" \
  --volume "$PWD/node_modules/:/app/node_modules/" \
  localhost/hlo:dev

[[ "$1" = "mount-perm" ]] && figlet -w 120 DEV-MOUNT-PERM && exec podman run \
  --init \
  --rm \
  --name hlo-dev \
  --env-file ./.env-dev \
  --publish 127.0.0.1:8005:8000 \
  --volume "$PWD/container/entrypoint.sh:/custom-entrypoint.sh" \
  --volume "$PWD/hlo/:/app/hlo/" \
  --volume "$PWD/static/:/app/static/" \
  --volume "$PWD/node_modules/:/app/node_modules/" \
  --volume /tank/tmp/hlo-dev/media/:/app/media_root/ \
  --volume /tank/tmp/hlo-dev/db/:/app/db/ \
  --volume /tank/tmp/hlo-dev/whoosh:/app/whoosh_index/ \
  localhost/hlo:dev

[[ "$1" = "dev-temp" ]] && figlet DEV-TEMP && exec podman run \
  --init \
  --rm \
  --name hlo-dev \
  --env-file ./.env-dev \
  --publish 127.0.0.1:8005:8000 \
  localhost/hlo:dev

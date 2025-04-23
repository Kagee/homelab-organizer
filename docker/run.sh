#! /bin/bash
cd "$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd .. # move to base dir
[[ "$1" = "mount-src" ]] && figlet DEV-MOUNT-RUN && exec podman run \
  --init \
  --rm \
  --name hlo-dev \
  --env-file ./.env-dev \
  --publish 127.0.0.1:8005:8000 \
  --volume "$PWD/docker/docker-entrypoint.sh:/custom-entrypoint.sh" \
  --volume "$PWD/hlo/:/app/hlo/" \
  localhost/hlo:dev

figlet DEBUG-RUN && exec podman run \
  --init \
  --rm \
  --name hlo-dev \
  --env-file ./.env-dev \
  --publish 127.0.0.1:8005:8000 \
  localhost/hlo:dev


# ENV HLO_STATIC_ROOT=/app/static_root
# ENV HLO_MEDIA_ROOT=/app/media_root
# ENV HLO_SQLITE3_FILE=/app/db/hlo.sqlite3
# ENV HLO_WHOOSH_INDEX=/app/whoosh_index

#figlet PROD-RUN && sudo podman run \
#  --init \
#  --rm \
#  --name hlo \
#  --env-file=./.env-prod \
#  --env HLO_DEBUG=false \
#  --env HLO_SQLITE3_FILE=/app/db/hlo.sqlite3 \
#  --env HLO_STATIC_ROOT=/app/static_root \
#  --env HLO_MEDIA_ROOT=/app/media_root \
#  --env HLO_WHOOSH_INDEX=/app/whoosh_index \
#  --volume /tank/data/hlo/static-test/:/app/static_root/ \
#  --volume /tank/data/hlo/media-test/:/app/media_root/ \
#  --volume /tank/data/hlo/db-test/:/app/db/ \
#  --volume /tank/data/hlo/whoosh-test/:/app/whoosh_index/ \
#  --publish 127.0.0.1:8000:8000 \
#  localhost/hlo:prod

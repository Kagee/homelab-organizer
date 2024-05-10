#! /usr/bin/env bash
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

cd "$SCRIPT_DIR"

CONTAINER_IMAGE="docker.io/bitnami/postgresql:16-debian-12"
CONTAINER_NAME="homelab-organizer-db"
# CONTAINER_NETWORK="homelab-organizer-net"
CONTAINER_VOLUME_FOLDER="postgresql-data/"
# For rootless podman, this can not be 127.0.0.1
CONTAINER_ENDPOINT="10.170.0.21:5432"

# Note! When POSTGRESQL_USERNAME is specified, 
# the postgres user is not assigned a password
# and as a result you cannot login remotely to
# the PostgreSQL server as the postgres user.
# If you still want to have access with the 
# user postgres, please set the 
# POSTGRESQL_POSTGRES_PASSWORD environment 
# variable

# POSTGRESQL_USERNAME=hlo
# POSTGRESQL_PASSWORD=
# POSTGRESQL_DATABASE=hlo
# POSTGRESQL_POSTGRES_PASSWORD=
# Or any of the container vars from above
set -a; source .env-db; set +a

mkdir -p "$CONTAINER_VOLUME_FOLDER";

# Using /usr/bin/dirname (keeps symlinks)
CONTAINER_VOLUME_FOLDER=$(cd "$CONTAINER_VOLUME_FOLDER"; pwd)
CONTAINER_INITDB_FOLDER=$(cd "postgresql-initdb.d/"; pwd)



if [ -z $POSTGRESQL_PASSWORD ]; then
    echo "You must at a minimum set POSTGRESQL_PASSWORD in .env-db" 1>&2;
    exit 1
fi

export POSTGRESQL_USERNAME="${POSTGRESQL_USERNAME:-hlo}"
export POSTGRESQL_DATABASE="${POSTGRESQL_DATABASE:-hlo}"
export POSTGRESQL_POSTGRES_PASSWORD="${POSTGRESQL_POSTGRES_PASSWORD:-}"

ENVSTR="--env POSTGRESQL_USERNAME --env POSTGRESQL_PASSWORD --env POSTGRESQL_DATABASE --env POSTGRESQL_POSTGRES_PASSWORD --env POSTGRESQL_TIMEZONE"

cd "$SCRIPT_DIR"

if [ "x$1" = "xclient" ]; then
    echo "Starting client ...";
    if ! podman container exists "$CONTAINER_NAME"; then
        echo "DB container is not running ($CONTAINER_NAME)" 1>&2;
        exit 1;
    fi
    #if ! podman network exists "$CONTAINER_NETWORK"; then
    #    echo "DB container network does not exist ($CONTAINER_NETWORK)" 1>&2;
    #    exit 1;
    #fi
    export PGPASSWORD="${POSTGRESQL_PASSWORD}"
    podman run -it --rm \
        --env PGPASSWORD \
        "$CONTAINER_IMAGE" \
            psql \
                --host "$(echo "$CONTAINER_ENDPOINT" | cut -d: -f1)" \
                --port "$(echo "$CONTAINER_ENDPOINT" | cut -d: -f2)" \
                --username "$POSTGRESQL_USERNAME";
    exit $?;
fi

if [ "x$1" != "xserver" ]; then
    echo "usage: $0 [server|client]" 1>&2
    exit 1;
fi

# https://github.com/containers/podman/blob/main/docs/tutorials/basic_networking.md

#echo "Starting network ..."
#podman network create --driver slirp4netns  "$CONTAINER_NETWORK"

echo "Starting server ..."
set -x

podman run -it \
    $ENVSTR \
    --rm \
    --name="$CONTAINER_NAME" \
    --publish="$CONTAINER_ENDPOINT:5432" \
    --volume="$CONTAINER_VOLUME_FOLDER:/bitnami/postgresql" \
    --volume "$CONTAINER_INITDB_FOLDER:/docker-entrypoint-initdb.d/" \
    "$CONTAINER_IMAGE";

# podman network rm "$CONTAINER_NETWORK"

exit $?;
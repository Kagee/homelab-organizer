#! /usr/bin/env bash
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

CONTAINER_IMAGE="docker.io/bitnami/postgresql:16-debian-12"
CONTAINER_NAME="homelab-organizer-db"
CONTAINER_NETWORK="homelab-organizer-net"
CONTAINER_VOLUME_FOLDER="postgresql-data/"

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
# POSTGRESQL_TIMEZONE="Europe/Oslo"
set -a; source .env-db; set +a

if [ -z $POSTGRESQL_PASSWORD ]; then
    echo "You must set POSTGRESQL_PASSWORD in .env-db" 1>&2;
    exit 1
fi

export POSTGRESQL_USERNAME="${POSTGRESQL_USERNAME:-hlo}"
export POSTGRESQL_DATABASE="${POSTGRESQL_DATABASE:-hlo}"
export POSTGRESQL_POSTGRES_PASSWORD="${POSTGRESQL_POSTGRES_PASSWORD:-}"
export POSTGRESQL_TIMEZONE="${POSTGRESQL_TIMEZONE:-'Europe/Oslo'}"

ENVSTR="--env POSTGRESQL_USERNAME --env POSTGRESQL_PASSWORD --env POSTGRESQL_DATABASE --env POSTGRESQL_POSTGRES_PASSWORD --env POSTGRESQL_TIMEZONE"

cd "$SCRIPT_DIR"

if [ "x$1" = "xclient" ]; then
    echo "Starting client ...";
    if ! podman container exists "$CONTAINER_NAME"; then
        echo "DB container is not running ($CONTAINER_NAME)" 1>&2;
        exit 1;
    fi
    if ! podman network exists "$CONTAINER_NETWORK"; then
        echo "DB container network does not exist ($CONTAINER_NETWORK)" 1>&2;
        exit 1;
    fi
    export PGPASSWORD="${POSTGRESQL_PASSWORD}"
    docker run -it --rm \
        --network "$CONTAINER_NETWORK" \
        --env PGPASSWORD \
        "$CONTAINER_IMAGE" \
            psql \
                -h "$CONTAINER_NAME" \
                -U "$POSTGRESQL_USERNAME";
    exit $?;
fi

if [ "x$1" != "xserver" ]; then
    echo "usage: $0 [server|client]" 1>&2
    exit 1;
fi

mkdir -p "$CONTAINER_VOLUME_FOLDER";


exit 1
https://github.com/containers/podman/blob/main/docs/tutorials/basic_networking.md
docker run \
    -v /path/to/postgresql-persistence:/bitnami/postgresql \
    bitnami/postgresql:latest

    docker run -d --name postgresql-server \
    --network app-tier \
    bitnami/postgresql:latest

echo "Starting server ..."
podamn run \
    $ENVSTR \
    --rm \
    --network "$CONTAINER_NETWORK" \
    "$CONTAINER_IMAGE";
    exit $?;
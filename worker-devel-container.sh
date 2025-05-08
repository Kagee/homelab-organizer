#! /bin/bash
cd "$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )" || exit

IMAGE="ubuntu-cf-worker:latest"
CONTAINER="ubuntu-cf-worker"
[[ "$1" = "build" ]] && {
podman container exists ${CONTAINER} && \
  podman stop ${CONTAINER};
exec podman build -f <(cat <<EOF
FROM ubuntu:24.04

RUN apt-get update && \
    apt-get -y install \
      nodejs \
      npm \
      vim \
      curl

WORKDIR /code
EOF
) --tag ${IMAGE} "${@:2}" .
}

[[ "$1" = "stop" ]] && \
  podman container exists ${CONTAINER} && \
  exec podman stop ${CONTAINER}

podman container exists ${CONTAINER} || podman run \
  --init \
  --rm \
  --detach \
  --name ${CONTAINER} \
  --volume "$PWD/cf-worker-code/:/code/worker/" \
  localhost/${IMAGE} \
    /bin/bash -c 'sleep infinity' && sleep 1

exec podman exec \
      --interactive \
      --tty  \
      ${CONTAINER} \
      /bin/bash

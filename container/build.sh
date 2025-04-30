#! /bin/bash
cd "$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd ..
[[ "$1" = "prod" ]] && \
  podman build -f container/Containerfile . --tag hlo:prod --build-arg=DEBUG_BUILD=false "${@:2}" && \
  podman save localhost/hlo:prod | sudo podman load && exit
exec podman build -f container/Containerfile . --tag hlo:dev --build-arg=DEBUG_BUILD=true "${@:2}"

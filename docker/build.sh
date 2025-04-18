#! /bin/bash
cd "$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd ..
[[ "$1" = "debug" ]] && exec podman build -f docker/Dockerfile . --tag hlo-debug --build-arg=DEBUG_BUILD=true "${@:2}"
podman build -f docker/Dockerfile . --tag hlo --build-arg=DEBUG_BUILD=false "$@"

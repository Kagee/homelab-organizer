#! /bin/bash
cd "$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd ..
podman run \
  --rm \
  --name hlo \
  --env HLO_SECRET_KEY=secret \
  --env HLO_CSRF_TRUSTED_ORIGINS='https://*' \
  --env HLO_REMOTE_USER_HEADER=REMOTE_USER \
  --env HLO_DEBUG=true \
  --publish 127.0.0.1:8005:8005 \
  localhost/hlo

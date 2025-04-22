#!/bin/bash
# https://github.com/mbentley/docker-runtime-user

[[ -f "/custom-entrypoint.sh" ]] && \
  [[ "$(basename "$0")" != "custom-entrypoint.sh" ]] && \
  echo "INFO: Running custom entrypoint" && \
  exec /custom-entrypoint.sh
set -e

# use specified user name or use `default` if not specified
APP_USERNAME="${APP_USERNAME:-default}"

# use specified group name or use the same user name also as the group name
APP_GROUP="${APP_GROUP:-${APP_USERNAME}}"

# App folder
APP_DIR="${APP_DIR:-/app}" 

# use the specified UID for the user
APP_UID="${APP_UID:-1000}"

# use the specified GID for the user
APP_GID="${APP_GID:-${APP_UID}}"

APP_SUPERUSER_EMAIL="${APP_SUPERUSER_EMAIL:-admin@admin.test}" 
APP_SUPERUSER_USERNAME="${APP_SUPERUSER_EMAIL:-${APP_SUPERUSER_EMAIL}}" 

# check to see if group exists; if not, create it
if grep -q -E "^${APP_GROUP}:" /etc/group > /dev/null 2>&1
then
  echo "INFO: Group ${APP_GROUP} exists; skipping creation"
else
  echo "INFO: Group ${APP_GROUP} doesn't exist; creating..."
  # create the group
  #   addgroup \
  #  --gid "${APP_GID}" \
  #  "${APP_GROUP}" || \
  set -x
  groupadd --gid "${APP_GID}" "${APP_GROUP}" || \
    (echo "INFO: Group ${APP_GROUP} exists but with a different name; renaming..."; \
      groupmod --gid "${APP_GID}" --new-name "${APP_GROUP}" \
      "$( \
        awk -F ':' '{print $1":"$3}' < /etc/group | grep ":${APP_GID}$" | awk -F ":" '{print $1}' \ 
      )")
  set +x
fi


# check to see if user exists; if not, create it
if id -u "${APP_USERNAME}" > /dev/null 2>&1
then
  echo "INFO: User ${APP_USERNAME} exists; skipping creation"
else
  echo "INFO: User ${APP_USERNAME} doesn't exist; creating..."
  # create the user
  set -x
  useradd \
    --no-log-init \
    --uid "${APP_UID}" \
    --gid "${APP_GID}" \
    --home-dir "/home/${APP_USERNAME}" \
    --create-home \
    --shell /bin/bash \
    "${APP_USERNAME}";
  set +x
fi

# change ownership of any directories needed to run my app as the proper UID/GID
echo "INFO: Setting permissions for ${APP_DIR} to ${APP_UID}:${APP_GID}"
chown "${APP_UID}:${APP_GID}" "${APP_DIR}"

# Cleanup permissions
#echo "INFO: Cleanup permissions in subdirectories of ${APP_DIR} to ${APP_UID}:${APP_GID}"
find "${APP_DIR}" -type d -not -perm 755 -exec chmod 755 {} \;
find "${APP_DIR}" -type f -not -perm 644 -not -path "/app/docker/*" -exec chmod 644 {} \;
find "${APP_DIR}" -not \( -uid "${APP_UID}" -and -gid "${APP_GID}" \) -not -path "/app/docker/*" -not -path "/app/hlo/*" -exec chown "${APP_UID}:${APP_GID}" {} \;

chmod 755 "${APP_DIR}/.venv/bin/gunicorn"

# start myapp
echo "INFO: Running app from ${APP_DIR} as ${APP_USERNAME}:${APP_GROUP} (${APP_UID}:${APP_GID})"

cd "${APP_DIR}"
# "Activate" venv for gunicorn etc
export PATH="${APP_DIR}/.venv/bin:$PATH"

# check for wrong permissions in /app/static_root /app/db /app/media_root /app/whoosh_index
echo "INFO: Running django migrations"
gosu "${APP_USERNAME}" python3 manage.py migrate

echo "INFO: Collecting static files"
set -x
gosu "${APP_USERNAME}" python3 manage.py collectstatic --no-input
set +x
# Whatever build, if we supply a command, run it.
[[ $# -ne 0 ]] && \
  cat /app/buildinfo && \
  echo "INFO: Custom command" && \
  set -x && \
  exec gosu "${APP_USERNAME}" "$@"

# $DEBUG_BUILD is alwasy `true` or `false`

# Use factory_boy and Faker to populate db and files
$DEBUG_BUILD && {
  # Fake test data
  echo "INFO: Creating fake app data"
  gosu "${APP_USERNAME}" python3 manage.py setup_test_data;

  # Create superuser
  echo "INFO: Creating superuser $APP_SUPERUSER_USERNAME ($APP_SUPERUSER_EMAIL)"
  gosu "${APP_USERNAME}" python3 manage.py createsuperuser \
  --username "$APP_SUPERUSER_USERNAME" \
  --email "$APP_SUPERUSER_EMAIL" \
  --noinput;

  # Exex as APP_USERNAME a development server on port 8000
  cat /app/buildinfo && \
    echo "INFO: Debug mode with runserver" && \
    exec gosu "${APP_USERNAME}" python3 manage.py runserver 0.0.0.0:8000
}
# exec as APP_USERNAME a production server on port 8000
$DEBUG_BUILD || cat /app/buildinfo && \
  echo "INFO: Production mode with gunicorn" && \
  exec gosu "${APP_USERNAME}" gunicorn hlo.wsgi:application -w 4 --bind 0.0.0.0:8000

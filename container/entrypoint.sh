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

# Start waitserver
cd "$APP_DIR"
echo "INFO: Starting temporary waitserver"
set -x
gunicorn --pid /app/waitserver.pid waitserver:application -b 0.0.0.0:8000 2>/dev/null 1>&2 &
{ set +x; } 2>/dev/null

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
  { set +x; } 2>/dev/null
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
  { set +x; } 2>/dev/null
fi

# change ownership of any directories needed to run my app as the proper UID/GID
echo "INFO: Setting permissions for ${APP_DIR} to ${APP_UID}:${APP_GID}"
chown "${APP_UID}:${APP_GID}" "${APP_DIR}"

# Cleanup permissions
echo "INFO: Cleanup permissions in subdirectories of ${APP_DIR} to ${APP_UID}:${APP_GID}"
FOLDERS=("${HLO_STATIC_ROOT}" "${HLO_MEDIA_ROOT}" "${HLO_WHOOSH_INDEX}" "$(dirname "${HLO_SQLITE3_FILE}")")

mkdir -p "${FOLDERS[@]}"

set -x
find "${FOLDERS[@]}" \
    -type d -not -perm 755 -exec chmod 755 {} \;
find "${FOLDERS[@]}" \
    -type f -not -perm 644  -exec chmod 644 {} \;
find "${FOLDERS[@]}" \
    -not \( -uid "${APP_UID}" -and -gid "${APP_GID}" \) \
    -exec chown "${APP_UID}:${APP_GID}" {} \;
{ set +x; } 2>/dev/null

# start myapp
echo "INFO: Running app from ${APP_DIR} as ${APP_USERNAME}:${APP_GROUP} (${APP_UID}:${APP_GID})"

cd "${APP_DIR}"
# "Activate" venv for gunicorn etc
set -x
export PATH="${APP_DIR}/.venv/bin:$PATH"
{ set +x; } 2>/dev/null

echo "INFO: Pre-run Dajngo checks"
set -x
gosu "${APP_USERNAME}" python3 manage.py check
{ set +x; } 2>/dev/null


echo "INFO: Running django migrations"
set -x
gosu "${APP_USERNAME}" python3 manage.py migrate --skip-checks
{ set +x; } 2>/dev/null

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
  set -x
  gosu "${APP_USERNAME}" python3 manage.py setup_test_data --skip-checks;
  { set +x; } 2>/dev/null

  # Create superuser
  echo "INFO: Creating superuser $APP_SUPERUSER_USERNAME ($APP_SUPERUSER_EMAIL)"
  set -x
  gosu "${APP_USERNAME}" python3 manage.py createsuperuser --skip-checks \
  --username "$APP_SUPERUSER_USERNAME" \
  --email "$APP_SUPERUSER_EMAIL" \
  --noinput 2>/dev/null || { set +x; } 2>/dev/null; echo "INFO: User $APP_SUPERUSER_USERNAME already existed";
  { set +x; } 2>/dev/null


  cat /app/buildinfo;

  # This is the absolute last time we can kill waitserver 
  echo "INFO: Terminating temporary waitserver"
  set -x
  kill "$(cat /app/waitserver.pid)";
  { set +x; } 2>/dev/null

  # Exex as APP_USERNAME a development server on port 8000
  echo "INFO: Starting debug mode with runserver";
  set -x
  exec gosu "${APP_USERNAME}" python3 manage.py runserver --skip-checks 0.0.0.0:8000;
}
# exec as APP_USERNAME a production server on port 8000
$DEBUG_BUILD || {
  echo "INFO: Collecting static files"
  gosu "${APP_USERNAME}" python3 manage.py collectstatic --no-input
  cat /app/buildinfo;
  echo "INFO: Production mode with gunicorn";
  kill "$(cat /app/waitserver.pid)";
  exec gosu "${APP_USERNAME}" gunicorn \
    --config /app/hlo/settings/gunicorn.conf.py;
}

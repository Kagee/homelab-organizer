#!/bin/sh
# https://github.com/mbentley/docker-runtime-user

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

# check to see if group exists; if not, create it
if grep -q -E "^${APP_GROUP}:" /etc/group > /dev/null 2>&1
then
  echo "INFO: Group ${APP_GROUP} exists; skipping creation"
else
  echo "INFO: Group ${APP_GROUP} doesn't exist; creating..."
  # create the group
  addgroup \
    --gid "${APP_GID}" \
    "${APP_GROUP}" || \
    (echo "INFO: Group ${APP_GROUP} exists but with a different name; renaming..."; \
      groupmod --gid "${APP_GID}" --new-name "${APP_GROUP}" \
      "$( \
        awk -F ':' '{print $1":"$3}' < /etc/group | grep ":${APP_GID}$" | awk -F ":" '{print $1}' \ 
      )")
fi


# check to see if user exists; if not, create it
if id -u "${APP_USERNAME}" > /dev/null 2>&1
then
  echo "INFO: User ${APP_USERNAME} exists; skipping creation"
else
  echo "INFO: User ${APP_USERNAME} doesn't exist; creating..."
  # create the user
  adduser --quiet \
    --uid "${APP_UID}" \
    --ingroup "${APP_GROUP}" \
    --home "/home/${APP_USERNAME}" \
    --shell /bin/sh \
    --disabled-password \
    "${APP_USERNAME}"
fi

# change ownership of any directories needed to run my app as the proper UID/GID
echo "INFO: Setting permissions for ${APP_DIR} to ${APP_UID}:${APP_GID}"
chown "${APP_UID}:${APP_GID}" "${APP_DIR}"

# Cleanup permissions
echo "INFO: Cleanup permissions in subdirectories of ${APP_DIR} to ${APP_UID}:${APP_GID}"
find "${APP_DIR}" -type d -not -perm 755 -exec chmod 755 {} \;
find "${APP_DIR}" -type f -not -perm 644 -exec chmod 644 {} \;
find "${APP_DIR}" -not \( -uid "${APP_UID}" -and -gid "${APP_GID}" \) -exec chown "${APP_UID}:${APP_GID}" {} \;

chmod 755 "${APP_DIR}/.venv/bin/gunicorn"

# start myapp
echo "INFO: Running app from ${APP_DIR} as ${APP_USERNAME}:${APP_GROUP} (${APP_UID}:${APP_GID})"

cd "${APP_DIR}"
# TODO:
export PATH="${APP_DIR}/.venv/bin:$PATH"

# check for wrong permissions in /app/static_root /app/db /app/media_root /app/whoosh_index
ls -lah /tmp
echo "INFO: Running django migrations"
gosu "${APP_USERNAME}" python3 manage.py migrate
ls -lah /tmp
echo "INFO: Collecting static files"
gosu "${APP_USERNAME}" python3 manage.py collectstatic
ls -lah /tmp
# exec and run the actual process specified in the CMD of the Dockerfile (which gets passed as ${*})
exec gosu "${APP_USERNAME}" "${@}"
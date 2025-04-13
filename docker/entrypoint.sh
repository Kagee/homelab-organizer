#!/bin/sh
# https://github.com/mbentley/docker-runtime-user

set -e

# use specified user name or use `default` if not specified
APP_USERNAME="${APP_USERNAME:-default}"

# use specified group name or use the same user name also as the group name
APP_GROUP="${APP_GROUP:-${APP_USERNAME}}"

# use the specified UID for the user
MY_UID="${MY_UID:-1000}"

# use the specified GID for the user
MY_GID="${MY_GID:-${MY_UID}}"


# check to see if group exists; if not, create it
if grep -q -E "^${APP_GROUP}:" /etc/group > /dev/null 2>&1
then
  echo "INFO: Group exists; skipping creation"
else
  echo "INFO: Group doesn't exist; creating..."
  # create the group
  addgroup -g "${MY_GID}" "${APP_GROUP}" || (echo "INFO: Group exists but with a different name; renaming..."; groupmod -g "${MY_GID}" -n "${APP_GROUP}" "$(awk -F ':' '{print $1":"$3}' < /etc/group | grep ":${MY_GID}$" | awk -F ":" '{print $1}')")
fi


# check to see if user exists; if not, create it
if id -u "${APP_USERNAME}" > /dev/null 2>&1
then
  echo "INFO: User exists; skipping creation"
else
  echo "INFO: User doesn't exist; creating..."
  # create the user
  adduser -u "${MY_UID}" -G "${APP_GROUP}" -h "/home/${APP_USERNAME}" -s /bin/sh -D "${APP_USERNAME}"
fi

# change ownership of any directories needed to run my app as the proper UID/GID
chown -R "${APP_USERNAME}:${APP_GROUP}" "/app"

# start myapp
echo "INFO: Running myapp as ${APP_USERNAME}:${APP_GROUP} (${MY_UID}:${MY_GID})"

cd /app
# TODO:
# ENV PATH="/app/.venv/bin:$PATH"
# check for wrong permissions in /app/static_root /app/db /app/media_root /app/whoosh_index
# gosu "${APP_USERNAME}" python3 manage.py migrate
# gosu "${APP_USERNAME}" python3 manage.py collectstatic

# exec and run the actual process specified in the CMD of the Dockerfile (which gets passed as ${*})
exec gosu "${APP_USERNAME}" "${@}"
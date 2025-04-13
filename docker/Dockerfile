#   _           _ _     _
#  | |__  _   _(_) | __| | ___ _ __
#  | '_ \| | | | | |/ _` |/ _ \ '__|
#  | |_) | |_| | | | (_| |  __/ |
#  |_.__/ \__,_|_|_|\__,_|\___|_|
#

FROM python:3.13 as builder
 
# Set the working directory inside the container
WORKDIR /app
 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 

# Create a venv that we can copy after building
RUN python3 -m venv .venv

# Use python binaries from venv
ENV PATH="/app/.venv/bin:$PATH"

# Upgrade pip
RUN pip install --upgrade pip 
 
# Copy the Django project requirements
COPY ../requirements.txt  /app/
 
# Install all dependencies
RUN pip install --no-cache-dir -r requirements.txt
 
RUN apt-get update && apt-get install -y npm

# Copy just what we need for a running app
COPY hlo /app/hlo
COPY static /app/static
COPY manage.py LICENSE pyproject.toml package.json /app/

# Install (download) JS deps to ./node_modules
RUN npm install .
# Convert all soft symlinks in static to hard symlinks (js and css from node_modules)
RUN find /app/static -type l -exec bash -c 'ln -f "$(readlink -m "$0")" "$0"' {} \;
# Remove the resto of the node data, as we now don't need it anymore
RUN rm -r ./node_modules

#      _    ____  ____
#     / \  |  _ \|  _ \
#    / _ \ | |_) | |_) |
#   / ___ \|  __/|  __/
#  /_/   \_\_|   |_|
#

FROM python:3.13-slim as app

# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 

# Copy venv, app code, static files etc from builder
COPY --from=builder /app /app
WORKDIR /app

ENV HLO_STATIC_ROOT=/app/static_root
ENV HLO_MEDIA_ROOT=/app/media_root
ENV HLO_SQLITE3_FILE=/app/db/hlo.sqlite3
ENV HLO_WHOOSH_INDEX=/app/whoosh_index

# Use python binaries from venv
ENV PATH="/app/.venv/bin:$PATH"

# Temporarily set some ENV vars that is required
# for manage.py check to work
RUN export \
    HLO_SECRET_KEY=no-so-secret-key-used-for-testing \
    HLO_CSRF_TRUSTED_ORIGINS='https://*' \
    HLO_REMOTE_USER_HEADER=none; \
    python3 manage.py check

# static_root is the static output directory
VOLUME /app/static_root /app/db /app/media_root /app/whoosh_index

ENTRYPOINT "entrypoint.sh"
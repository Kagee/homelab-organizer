# Use the official Python runtime image
FROM python:3.13 as builder
 
# Create the app directory
RUN mkdir /app
 
# Set the working directory inside the container
WORKDIR /app
 
# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 

RUN python3 -m venv .venv
ENV PATH="/app/.venv/bin:$PATH"

# Upgrade pip
RUN pip install --upgrade pip 
 
# Copy the Django project  and install dependencies
COPY ../requirements.txt  /app/
 
# run this command to install all dependencies  --root-user-action=ignore 
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy the Django project to the container

RUN ls -lah
RUN apt-get update && apt-get install -y npm

# We copy static in the next build step
COPY hlo /app/hlo
COPY static /app/static
copy manage.py LICENSE pyproject.toml package.json /app
RUN npm install . && ls

FROM python:3.13-slim as app

COPY --from=builder /app /app
WORKDIR /app

# static_root is the static output directory
VOLUME /app/static_root /app/db /app/media_root /app/whoosh_index

RUN ls


RUN cat static/bootstrap/bootstrap.min.css

RUN ls -lah static/bootstrap
# Enable venv

ENV PATH="/app/.venv/bin:$PATH"
RUN pip freeze

EXPOSE 8000

ENTRYPOINT "entrypoint.sh"

#CMD ["python", "app.py", ]# Run Django’s development server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


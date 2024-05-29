import environ
from django.core.management.commands.runserver import Command as Runserver

env = environ.FileAwareEnv()
env.prefix = "HLO_"

Runserver.default_port = env.int("RUNSERVER_PORT", default=8005)
Runserver.default_addr = env.int("RUNSERVER_BIND", default="0.0.0.0")  # noqa: S104

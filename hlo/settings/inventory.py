import environ  # type: ignore

env = environ.FileAwareEnv()

env.prefix = "IN_"

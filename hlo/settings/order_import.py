import environ  # type: ignore

env = environ.FileAwareEnv()

env.prefix = "OI_"

DATA_FOLDER = env.list("DATA_FOLDER", default=[])

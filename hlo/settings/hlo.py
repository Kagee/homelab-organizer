from pathlib import Path

import environ

env = environ.FileAwareEnv()
env.prefix = "HLO_"

INPUT_FOLDER: Path = Path(
        env("INPUT_FOLDER", default="./input"),
    ).resolve()

JSON_SCHEMA: Path = Path(
        env("JSON_SCHEMA", default="./schema/webshop-orders.json"),
    ).resolve()

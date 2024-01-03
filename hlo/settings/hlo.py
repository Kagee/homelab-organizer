from pathlib import Path
import environ  # type: ignore

env = environ.FileAwareEnv()

INPUT_FOLDER: Path = Path(
        env("INPUT_FOLDER", default="./input")
    ).resolve()

JSON_SCHEMA: Path = Path(
        env("JSON_SCHEMA", default="./schema/webshop-orders.json")
    ).resolve()
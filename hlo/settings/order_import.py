from pathlib import Path
import environ  # type: ignore

env = environ.FileAwareEnv()

env.prefix = "OI_"

IMPORT_FOLDER: Path = Path(
        env("IMPORT_FOLDER", default="./import")
    ).resolve()

JSON_SCHEMA: Path = Path(
        env("JSON_SCHEMA", default="./import/schema.json")
    ).resolve()

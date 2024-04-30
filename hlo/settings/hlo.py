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

# Instance of https://github.com/dersimn/brother_ql_web or a fork
# with a simmilar api endpoint for printing images
BQW_ENDPOINT: str = env("BQW_ENDPOINT", default=None)

QR_URL_PREFIX: str = env("QR_URL_PREFIX", default="")

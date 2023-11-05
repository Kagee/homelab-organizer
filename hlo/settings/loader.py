from pathlib import Path
import environ  # type: ignore

env = environ.FileAwareEnv()

env.prefix = "LO_"

INPUT_FOLDER: Path = Path(
        env("INPUT_FOLDER", default="./input")
    ).resolve()

JSON_SCHEMA: Path = Path(
        env("JSON_SCHEMA", default="./schema/webshop-orders.json")
    ).resolve()

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': './whoosh_index' 
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
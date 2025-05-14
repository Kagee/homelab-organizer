from pathlib import Path

import environ

env = environ.FileAwareEnv()
env.prefix = "HLO_"

WHOOSH_INDEX = Path(env("WHOOSH_INDEX", default="./whoosh_index")).resolve()

HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": WHOOSH_INDEX,
    },
}
HAYSTACK_SIGNAL_PROCESSOR = "haystack.signals.RealtimeSignalProcessor"

# djmoney valid currencies
CURRENCIES = ("USD", "EUR", "NOK", "JPY")
# djmoney currencies labels
CURRENCY_CHOICES = [("USD", "$"), ("EUR", "€"), ("NOK", "kr"), ("JPY", "¥")]

SELECT2_THEME = "bootstrap-5"

FACTORY_SEED = env("FACTORY_SEED", default="hlo-testing-seed")

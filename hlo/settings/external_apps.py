import environ

env = environ.FileAwareEnv()
env.prefix = "HLO_"

HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": "./whoosh_index",
    },
}
HAYSTACK_SIGNAL_PROCESSOR = "haystack.signals.RealtimeSignalProcessor"

# djmoney valid currencies
CURRENCIES = ("USD", "EUR", "NOK", "JPY")
# djmoney currencies labels
CURRENCY_CHOICES = [("USD", "$"), ("EUR", "€"), ("NOK", "kr"), ("JPY", "¥")]

SELECT2_THEME = "bootstrap-5"

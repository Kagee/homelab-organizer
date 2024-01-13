import environ  # type: ignore

env = environ.FileAwareEnv()
env.prefix = "HLO_"

HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": "./whoosh_index",
    },
}
HAYSTACK_SIGNAL_PROCESSOR = "haystack.signals.RealtimeSignalProcessor"

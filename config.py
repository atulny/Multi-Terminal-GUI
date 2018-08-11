from json import dumps, loads

import log
from util import Dict

CONFIG = Dict(
    log_level=0
)


def load_config():
    try:
        with open("config.json") as i:
            data = loads(i.read())

            for key in data.keys():
                CONFIG[key] = data.get(key)

    except FileNotFoundError as e:
        log.info("Configuration file not found, generating one now.")
        data = dumps(CONFIG, indent=4)
        with open("config.json", 'w') as i:
            i.write(data)
        log.info("Please configure configuration file before executing again.")
        exit(1)

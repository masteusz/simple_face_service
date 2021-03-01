import os

from utils import load_as_dictionary

config = load_as_dictionary(os.environ.get("CONFIG_PATH", "config/config.yaml"))

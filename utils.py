import json
import os

CONFIG_PATH = "config.json"

DEFAULT_CONFIG = {
    "api_key": "",
    "groq_key": "",
    "serpapi_key": "",
    "save_location": "generated_presentations"
}

def load_config():
    """Loads config.json safely. Creates default file if missing."""
    if not os.path.exists(CONFIG_PATH):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except:
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG


def save_config(data):
    """Saves config.json."""
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=4)


def update_key(key_name, value):
    """Updates a single config key (api_key, groq_key, serpapi_key)."""
    cfg = load_config()
    cfg[key_name] = value
    save_config(cfg)

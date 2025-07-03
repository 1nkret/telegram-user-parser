import configparser
import os
import sys

SECTION = "Telegram"


def get_hidden_dir():
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    hidden_dir = os.path.join(os.path.expanduser("~"), ".telegram_parser")
    os.makedirs(hidden_dir, exist_ok=True)

    if os.name == 'nt':
        os.system(f'attrib +h "{hidden_dir}"')

    return hidden_dir


def get_config_path():
    return os.path.join(get_hidden_dir(), "config.ini")


CONFIG_PATH = get_config_path()


def load_config():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_PATH):
        config.read(CONFIG_PATH, encoding="utf-8")
    return {
        "api_id": config.get(SECTION, "api_id", fallback=""),
        "api_hash": config.get(SECTION, "api_hash", fallback=""),
        "phone": config.get(SECTION, "phone", fallback=""),
        "password": config.get(SECTION, "password", fallback=""),
        "target_channel": config.get(SECTION, "target_channel", fallback=""),
    }


def save_config(data: dict):
    config = configparser.ConfigParser()
    config[SECTION] = {
        "api_id": data.get("api_id", ""),
        "api_hash": data.get("api_hash", ""),
        "phone": data.get("phone", ""),
        "password": data.get("password", ""),
        "target_channel": data.get("target_channel", "")
    }
    with open(CONFIG_PATH, "w", encoding="utf-8") as configfile:
        config.write(configfile)

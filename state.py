import json
import os
from config import STATE_FILE


def load_state():
    if not os.path.exists(STATE_FILE):
        return {}

    with open(STATE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_state(data):
    with open(STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

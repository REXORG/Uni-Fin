import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "data"


def load_content():
    with open(BASE / "content_items.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_users():
    with open(BASE / "users.json", "r", encoding="utf-8") as f:
        return json.load(f)

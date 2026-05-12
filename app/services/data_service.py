import json
from pathlib import Path
from typing import Any, List

APP_DATA_DIR = Path(__file__).resolve().parents[1] / "data"
REPO_ROOT = Path(__file__).resolve().parents[2]
DATASET_DIR = REPO_ROOT / "dataset"


def _load_json_first_available(candidates: List[Path]) -> Any:
    for path in candidates:
        if path.exists() and path.is_file():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    checked = "\n - ".join(str(p) for p in candidates)
    raise FileNotFoundError(f"JSON file not found. Checked paths:\n - {checked}")


def load_content():
    return _load_json_first_available([
        APP_DATA_DIR / "content_items.json",
        REPO_ROOT / "app" / "data" / "content_items.json",
    ])


def load_users():
    return _load_json_first_available([
        APP_DATA_DIR / "users.json",
        REPO_ROOT / "app" / "data" / "users.json",
    ])

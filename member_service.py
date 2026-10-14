import json
from datatime import datatime
from pathlib import Path

DATA_FILE = Path("data") / "members.json"

def save_members(members):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            members, file, indent=4, ensure_ascii=False
        )

def load_members():
    if not DATA_FILE.exists():
        return[]
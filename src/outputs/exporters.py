thonpython
import json
import csv
from pathlib import Path

def export_json(data, filepath: str):
    Path(filepath).parent.mkdir(exist_ok=True, parents=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def export_csv(data, filepath: str):
    if not data:
        return
    Path(filepath).parent.mkdir(exist_ok=True, parents=True)
    keys = data[0].keys()

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
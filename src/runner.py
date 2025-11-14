thonpython
import json
import logging
from pathlib import Path

import requests

from extractors.reddit_parser import parse_reddit_post
from outputs.exporters import export_json, export_csv

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def read_input_file(path: str):
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def fetch_json(url: str):
    try:
        if not url.endswith(".json"):
            url = url.rstrip("/") + ".json"
        resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        logging.error(f"Failed to fetch {url}: {e}")
        return None

def main():
    inputs = read_input_file("data/inputs.sample.txt")
    results = []

    for url in inputs:
        logging.info(f"Processing: {url}")
        data = fetch_json(url)
        if not data:
            continue

        parsed = parse_reddit_post(data, url)
        results.extend(parsed)

    Path("output").mkdir(exist_ok=True)
    export_json(results, "output/results.json")
    export_csv(results, "output/results.csv")

    logging.info("Scraping completed.")

if __name__ == "__main__":
    main()
import csv
from typing import Iterator


def read_csv(path: str) -> Iterator[dict]:
    """Yield raw rows from a CSV as dicts."""
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row

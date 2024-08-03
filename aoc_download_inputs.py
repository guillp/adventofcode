"""This downloads all inputs from AoC."""

import os
import sys
from pathlib import Path

import requests

if __name__ == "__main__":
    try:
        cookie = os.getenv("ADVENTOFCODE_SESSION")
        assert cookie is not None
    except Exception:
        print("Please set ADVENTOFCODE_SESSION envvar with your adventofcode.com session cookie value.")
        sys.exit(1)

    session = requests.Session()
    session.cookies["session"] = cookie

    for year in range(2015, 2025):
        root = Path(f"aoc{year}")
        root.mkdir(parents=True, exist_ok=True)

        for day in range(1, 26):
            content = session.get(f"https://adventofcode.com/{year}/day/{day}/input").content
            with (root / f"{day:02d}.txt").open("wb") as f:
                f.write(content)

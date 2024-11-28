"""This fetches all the answers you already provided in AoC, and show which answers are missing.
This produces files named "aocYEAR/DD.ans" (e.g aoc2020/18.ans) for each day of each year."""

import os
import re
import sys
from pathlib import Path

import requests

if __name__ == "__main__":
    try:
        cookie = os.getenv("ADVENTOFCODE_SESSION") or sys.argv[1]
        assert cookie is not None
    except (KeyError, AssertionError):
        print("Please set ADVENTOFCODE_SESSION envvar with your adventofcode.com session cookie value.")
        sys.exit(1)

    session = requests.Session()
    session.cookies["session"] = cookie
    del session.headers["User-Agent"]
    for year in range(2015, 2099):
        root = Path(f"aoc{year}")
        root.mkdir(parents=True, exist_ok=True)
        for day in range(1, 26):
            url = f"https://adventofcode.com/{year}/day/{day}"
            resp = session.get(url)
            if resp.status_code == 404:
                sys.exit(0)
            answers = re.findall("<p>Your puzzle answer was <code>(.*?)</code>", resp.text)
            with (root / f"{day:02d}.ans").open("wt") as f:
                for answer in answers:
                    f.write(answer)
                    f.write("\n")
            match len(answers):
                case 0:
                    print("Missing Part1:", url)
                case 1 if day != 25:
                    print("Missing Part2:", url)

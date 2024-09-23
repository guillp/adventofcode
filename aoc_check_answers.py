"""This executes all solutions for all days and checks that the answers are equal to those in .ans files.
If the solution matches, store the SHA256 of the solution file into a .s256 file. This avoids running the
same working solution multiple times (since some files take a while to run).
"""

import hashlib
import os
import subprocess
import sys
import time
from pathlib import Path


def calc_file_hash(filepath: Path) -> str:
    with filepath.open("rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


if __name__ == "__main__":
    for year in range(2015, 2024):
        root = Path(f"aoc{year}")
        os.chdir(root)
        for day in range(1, 26):
            stem = Path(f"{day:02d}")
            day_hash = stem.with_suffix(".s256")
            day_solution = stem.with_suffix(".py")
            day_answers = stem.with_suffix(".ans")

            if not day_solution.exists():
                print(
                    f"{year} day {day}: Missing solution (in file '{day_solution}'): https://adventofcode.com/{year}/day/{day}",
                )
                continue

            current_filehash = calc_file_hash(day_solution)

            if day_hash.exists() and day_solution.exists():
                with open(day_hash) as f:
                    stored_filehash = f.read().strip()
                if current_filehash == stored_filehash:
                    if "-v" in sys.argv:
                        print(f"{year} day {day}: OK - previously verified")
                    continue

            if not day_answers.exists():
                print(f"{year} day {day}: Missing answers (in file '{day_answers}')")
                continue
            with day_answers.open("rt") as f:
                good_answers = f.read().split()

            t0 = time.perf_counter()
            try:
                process = subprocess.run(["python", day_solution], capture_output=True, check=False)
            except KeyboardInterrupt:
                print(f"{year} day {day}: interrupted after {time.perf_counter() - t0} s")
                sys.exit()

            your_answers = process.stdout.decode().split()
            if good_answers != your_answers:
                print(
                    f"{year} day {day}: WRONG -",
                    your_answers,
                    ", expected:",
                    good_answers,
                    f": https://adventofcode.com/{year}/day/{day}",
                )
            else:
                if "-v" in sys.argv:
                    print(f"{year} day {day}: OK in {time.perf_counter()-t0} s")
                with day_hash.open("wt") as f:
                    f.write(current_filehash)

        os.chdir("..")

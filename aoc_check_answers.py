"""This executes all programs for all days and check that the answers are equal to those in .ans files."""

import os
import subprocess
from pathlib import Path

if __name__ == "__main__":
    for year in range(2015, 2024):
        root = Path(f"aoc{year}")
        os.chdir(root)
        for day in range(1, 26):
            print(f"{year} day {day}: ", end="")

            with Path(f"{day:02d}.ans").open("rt") as f:
                good_answers = f.read().split()
            day_solution = f"{day:02d}.py"
            if not Path(day_solution).exists():
                print(f"Missing solution for {year} day {day}")
                continue

            process = subprocess.run(["python", day_solution], capture_output=True)
            your_answers = process.stdout.decode().split()
            if good_answers != your_answers:
                print("WRONG -", your_answers, ", expected:", good_answers)
            else:
                print("OK")
        os.chdir("..")

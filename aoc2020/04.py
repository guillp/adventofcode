import re


def solve(content: str) -> tuple[int, int]:
    part1 = part2 = 0
    for passport in content.strip().split("\n\n"):
        fields = dict(field.split(":") for field in passport.split())
        if not {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}.issubset(fields):
            continue

        part1 += 1
        try:
            assert re.match(r"^\d{4}$", fields["byr"])
            assert 1920 <= int(fields["byr"]) <= 2002
            assert re.match(r"^\d{4}$", fields["iyr"])
            assert 2010 <= int(fields["iyr"]) <= 2020
            assert re.match(r"^\d{4}$", fields["eyr"])
            assert 2020 <= int(fields["eyr"]) <= 2030
            hgt = fields["hgt"]
            if hgt.endswith("cm"):
                assert 150 <= int(hgt.removesuffix("cm")) <= 193
            elif hgt.endswith("in"):
                assert 59 <= int(hgt.removesuffix("in")) <= 76
            else:
                assert False
            assert re.match(r"^#[0-9a-f]{6}$", fields["hcl"])
            assert fields["ecl"] in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
            assert re.match(r"^\d{9}$", fields["pid"])
        except Exception:
            continue
        else:
            part2 += 1

    return part1, part2


test_input = """\
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
"""

assert solve(test_input) == (2, 2)
# assert solve(test_input, part2=True) == SOL2

with open("04.txt") as f:
    content = f.read()

for part in solve(content):
    print(part)

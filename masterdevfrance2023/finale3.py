import sys

N = int(input())
themes = [input().split() for _ in range(N)]


def debug(*args: object) -> None:
    print(*args, file=sys.stderr)


debug(f"{N} stands, with themes:")
debug(*(themes[i][0].ljust(16, ".") for i in range(N)))
debug(*(themes[i][1].ljust(16, ".") for i in range(N)))
debug()

if N == 1:
    print(2)
else:
    total = 0
    for first_theme in (0, 1):
        debug(f"With first theme {themes[0][first_theme]} ...")
        s = [[0, 0] for _ in range(N)]
        s[0][first_theme] = 1
        for current_stand in range(1, N):
            debug(f"* at stand {current_stand} with themes {themes[current_stand]}")
            for previous_theme, current_theme in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                if s[current_stand - 1][previous_theme] == 0:
                    continue
                if themes[current_stand][current_theme] != themes[current_stand - 1][previous_theme]:
                    s[current_stand][current_theme] += s[current_stand - 1][previous_theme]
                    debug(
                        f"... can do theme {themes[current_stand][current_theme]}"
                        f" after previous theme {themes[current_stand-1][previous_theme]}, {s=}",
                    )

        for last_theme in (0, 1):
            if themes[N - 1][last_theme] != themes[0][first_theme]:
                debug(
                    f"... can do first theme {themes[0][first_theme]}"
                    f" after last_theme {themes[N-1][last_theme]},"
                    f" adding {s[N-1][last_theme]} possibilities",
                )
                total += s[N - 1][last_theme]

    print(total)

debug("=========\n")

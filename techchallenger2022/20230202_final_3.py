from collections import defaultdict

slopes = defaultdict(float)
"this will contain every derivative (slope) at any integer X coordinate"

# read the upper part, calc the slopes at each X integer coordinate
x1 = y1 = 0
for _ in range(int(input())):
    x2, y2 = (int(x) for x in input().split())
    slope = (y2 - y1) / (x2 - x1)
    for x in range(x1, x2):
        slopes[x] += slope
    x1, y1 = x2, y2

# combine the slopes from the bottom part to those of the upper part
x1 = y1 = 0
for _ in range(int(input())):
    x2, y2 = (int(x) for x in input().split())
    slope = (y1 - y2) / (x2 - x1)
    for x in range(x1, x2):
        slopes[x] += slope
    x1, y1 = x2, y2

# now we have the slopes from the whole cake,
# we can calc the total area of the cake
total_area = y = 0.0
# plus a helper dict that will map current_area -> (x, y, slope)
# which we will use below
areas = {}
for x, slope in slopes.items():
    areas[total_area] = x, y, slope
    total_area += y + slope / 2
    y += slope


def solve(target_area: float) -> float:
    """Calc the X coordinate where we need to cut to get a given target area"""

    for area, (x, y, slope) in reversed(areas.items()):
        if area < target_area:
            break
    remaining = target_area - area
    # we need to find X so that the area: X * (y+X*slope/2) is equal to remaining
    # this equation can be written like: (slope/2 * X²) + y*X - mod = 0
    # this is a second degree equation (a*x² + b*x + c == 0), which can be solved
    # by applying Bhaskara with: a = slope/2 , b = y , c = -mod
    delta = (y**2 + 4 * slope / 2 * remaining) ** 0.5
    x1 = (-y + delta) / slope
    x2 = (-y - delta) / slope

    return x + x1 if 0 <= x1 < 1 else x2


print(solve(total_area / 3))
print(solve(2 * total_area / 3))

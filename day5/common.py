EXAMPLE = """
3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""


def parse_input(text):
    lines = [ln.strip() for ln in text]
    ranges = []
    ids = []

    i = 0
    # read ranges until blank line
    while i < len(lines) and lines[i] != "":
        a, b = lines[i].split("-")
        ranges.append((int(a), int(b)))
        i += 1

    # skip blank lines
    while i < len(lines) and lines[i] == "":
        i += 1

    # read ids
    while i < len(lines):
        if lines[i] != "":
            ids.append(int(lines[i]))
        i += 1

    return ranges, ids


def merge_ranges(ranges):
    if not ranges:
        return []

    ranges = sorted(ranges)  # sort by start, then end
    merged = []
    cur_lo, cur_hi = ranges[0]

    for lo, hi in ranges[1:]:
        if lo <= cur_hi + 1:  # overlaps or touches
            if hi > cur_hi:
                cur_hi = hi
        else:
            merged.append((cur_lo, cur_hi))
            cur_lo, cur_hi = lo, hi

    merged.append((cur_lo, cur_hi))
    return merged


def is_fresh(merged, x):
    # binary search for interval with lo <= x <= hi
    lo = 0
    hi = len(merged) - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        a, b = merged[mid]
        if x < a:
            hi = mid - 1
        elif x > b:
            lo = mid + 1
        else:
            return True

    return False


def total_covered(merged):
    total = 0
    for lo, hi in merged:
        total += hi - lo + 1
    return total

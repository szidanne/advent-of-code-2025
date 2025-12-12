import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aoc_common import parse_example, read_input
from day5.common import EXAMPLE, parse_input, merge_ranges, is_fresh


def solve(text):
    ranges, ids = parse_input(text)
    merged = merge_ranges(ranges)

    count = 0
    for x in ids:
        if is_fresh(merged, x):
            count += 1
    return count


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "example":
        data = parse_example(EXAMPLE)
    else:
        data = read_input()

    print(solve(data))

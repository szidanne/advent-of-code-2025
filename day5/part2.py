import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aoc_common import parse_example, read_input
from day5.common import EXAMPLE, parse_input, merge_ranges, total_covered


def solve(text):
    ranges, _ = parse_input(text)
    merged = merge_ranges(ranges)
    return total_covered(merged)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "example":
        data = parse_example(EXAMPLE)
    else:
        data = read_input()

    print(solve(data))

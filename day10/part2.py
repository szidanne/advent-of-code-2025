import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aoc_common import parse_example, read_input
from day10.common import EXAMPLE, solve_part2


def solve(lines):
    return solve_part2(lines)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "example":
        data = parse_example(EXAMPLE)
    else:
        data = read_input()

    print(solve(data))

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aoc_common import parse_example, read_input
from day9.common import EXAMPLE, read_points, max_area_red_corners_inside_loop


def solve(lines):
    points_in_order = read_points(lines)
    return max_area_red_corners_inside_loop(points_in_order)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "example":
        data = parse_example(EXAMPLE)
    else:
        data = read_input()

    print(solve(data))

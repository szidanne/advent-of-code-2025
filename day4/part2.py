import sys
from pathlib import Path

# --- add repo root to sys.path so we can import aoc_common.py ---
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aoc_common import parse_example, read_input
from day4.common import EXAMPLE, remove_all_accessible


def solve(lines):
    # mutable grid
    grid = [list(line.strip()) for line in lines if line.strip()]
    return remove_all_accessible(grid)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "example":
        data = parse_example(EXAMPLE)
    else:
        data = read_input()

    print(solve(data))

import sys

from pathlib import Path

# --- add repo root to sys.path so we can import aoc_common.py ---
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aoc_common import parse_example, read_input
from day3.common import (
    EXAMPLE,
    best_k_digits,
)

k = 12


def solve(lines):
    # print(lines)
    total = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        total += best_k_digits(line, k)
    return total


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "example":
        data = parse_example(EXAMPLE)
    else:
        data = read_input()

    answer = solve(data)
    print(answer)

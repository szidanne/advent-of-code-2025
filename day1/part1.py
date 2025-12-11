import sys

from pathlib import Path

# --- add repo root to sys.path so we can import aoc_common.py ---
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aoc_common import parse_example, read_input
from day1.common import DIAL_SIZE, EXAMPLE, START, parse_move


# solving
def solve(lines):
    pos = START
    hits_zero = 0

    for raw in lines:
        parsed = parse_move(raw)
        if parsed is None:
            continue

        direction, steps = parsed
        move = -steps if direction == "L" else steps

        pos = (pos + move) % DIAL_SIZE

        if pos == 0:
            hits_zero += 1

    return hits_zero


if __name__ == "__main__":
    # example override
    if len(sys.argv) > 1 and sys.argv[1] == "example":
        data = parse_example(EXAMPLE)
    else:
        data = read_input()

    ans = solve(data)
    print(ans)

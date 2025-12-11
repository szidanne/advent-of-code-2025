import sys

from pathlib import Path

# --- add repo root to sys.path so we can import aoc_common.py ---
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aoc_common import parse_example, read_input
from day1.common import DIAL_SIZE, EXAMPLE, START, parse_move


def count_hits_during_move(pos, direction, steps, dial_size):
    if steps == 0:
        return 0

    if direction == "R":
        # pos + k ≡ 0 (mod N)
        r = (-pos) % dial_size
        k0 = dial_size if r == 0 else r
    else:
        # direction == "L"
        # pos - k ≡ 0 (mod N)
        r = pos % dial_size
        k0 = dial_size if r == 0 else r

    if k0 > steps:
        return 0

    return 1 + (steps - k0) // dial_size


def solve(lines):
    pos = START
    hits_zero = 0

    for raw in lines:
        move = parse_move(raw)
        if move is None:
            continue

        direction, steps = move

        hits_zero += count_hits_during_move(pos, direction, steps, DIAL_SIZE)

        if direction == "R":
            pos = (pos + steps) % DIAL_SIZE
        else:
            pos = (pos - steps) % DIAL_SIZE

    return hits_zero


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "example":
        data_lines = parse_example(EXAMPLE)
    else:
        data_lines = read_input()

    answer = solve(data_lines)
    print(answer)

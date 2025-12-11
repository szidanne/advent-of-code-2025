import sys

from pathlib import Path

# --- add repo root to sys.path so we can import aoc_common.py ---
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aoc_common import parse_example, read_input
from day2.common import (
    EXAMPLE,
    parse_ranges,
    generate_repeated_block_ids,
    id_in_any_range,
)


def sum_invalid_ids_part2(line):
    ranges = parse_ranges(line)
    global_min = None
    for r in ranges:
        lo = r[0]
        if global_min is None or lo < global_min:
            global_min = lo

    # find largest 'hi'
    global_max = None
    for r in ranges:
        hi = r[1]
        if global_max is None or hi > global_max:
            global_max = hi

    candidates = generate_repeated_block_ids(global_min, global_max)

    total = sum(n for n in candidates if id_in_any_range(n, ranges))
    return total


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "example":
        data = parse_example(EXAMPLE, splitlines=False)
    else:
        data = read_input(splitlines=False)

    print(sum_invalid_ids_part2(data))

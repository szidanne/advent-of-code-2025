import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aoc_common import parse_example, read_input
from day6.common import EXAMPLE, to_int, apply_op, not_empty, read_for_part1


def solve(lines):
    grid = read_for_part1(lines)

    # operator row is last line
    ops_row = grid[-1]
    num_rows = grid[:-1]

    # print(ops_row, num_rows)

    # find operator positions (their column indices)
    op_positions = []
    for i, ch in enumerate(ops_row):
        if ch in ("+", "*"):
            op_positions.append((i, ch))

    results = []

    # print(op_positions)

    # for each operator, grab the "number in that column" from each row
    for col, op in op_positions:
        nums = []

        for row in num_rows:
            # safe if some rows are shorter
            if col >= len(row):
                continue
            if not row[col].isdigit():
                continue

            nums.append(to_int(row[col]))

        results.append(apply_op(op, nums))

    # grand total is sum of per-problem results
    total = 0
    for x in results:
        total += x
    return total


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "example":
        data = parse_example(EXAMPLE)
    else:
        data = read_input()

    print(solve(data))

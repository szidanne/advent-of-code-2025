import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aoc_common import parse_example, read_input
from day6.common import (
    EXAMPLE,
    apply_op,
    to_int,
    read_padded_grid,
    split_problem_blocks,
)


def solve(lines):
    grid = read_padded_grid(lines)

    blocks = split_problem_blocks(grid)
    ops = []

    total = 0
    last_row = len(grid) - 1  # operator row
    num_rows_end = last_row  # rows above operator row

    for start, end in blocks:
        # operator is the + or * inside this block on the bottom row
        op = None
        for c in range(start, end):
            ch = grid[last_row][c]
            if ch in ("+", "*"):
                op = ch
                break
        if op is None:
            raise ValueError("No operator found in a block.")
        ops.append(op)

        # part 2 numbers: read digit-columns RIGHT -> LEFT inside the block
        nums = []
        for c in range(end - 1, start - 1, -1):
            digits = []
            for r in range(0, num_rows_end):
                ch = grid[r][c]
                if ch.isdigit():
                    digits.append(ch)
            if digits:
                nums.append(to_int(digits))

        total += apply_op(op, nums)

    # print("ops =", ops)

    return total


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "example":
        data = parse_example(EXAMPLE)
    else:
        data = read_input()

    print(solve(data))

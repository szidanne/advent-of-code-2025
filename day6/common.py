EXAMPLE = """
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
""".rstrip(
    "\n"
)


def not_empty(s):
    return s != "" and s != " " and s != "\n" and s is not None


def filter_not_empty(arr):
    return list(filter(not_empty, arr))


def apply_op(op, nums):
    if op == "+":
        total = 0
        for x in nums:
            total += x
        return total
    if op == "*":
        total = 1
        for x in nums:
            total *= x
        return total
    raise ValueError(f"Unknown operator: {op!r}")


def to_int(digits):
    # digits like ['1','2','3'] -> 123
    return int("".join(digits))


def read_for_part1(lines):
    # turns each line into tokens split by spaces
    # ex: "123 328  51" -> ["123","328","51"]
    out = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        out.append(line.split())
    return out


def read_padded_grid(lines):
    # keep columns; pad each line to same width
    raw = [line.rstrip("\n") for line in lines if line.rstrip("\n") != ""]
    width = max(len(line) for line in raw) if raw else 0
    grid = []
    for line in raw:
        grid.append(list(line.ljust(width)))
    return grid


def split_problem_blocks(grid):
    # returns list of (start_col, end_col) blocks
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    def col_is_blank(c):
        for r in range(rows):
            if grid[r][c] != " ":
                return False
        return True

    blocks = []
    c = 0
    while c < cols:
        while c < cols and col_is_blank(c):
            c += 1
        if c >= cols:
            break
        start = c
        while c < cols and not col_is_blank(c):
            c += 1
        end = c
        blocks.append((start, end))
    return blocks

EXAMPLE = """
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
""".strip()


def is_valid_line(s):
    return s is not None and s != ""


def read_grid(lines):
    # keep dots/spaces exactly; just drop empty lines
    rows = [r.rstrip("\n") for r in lines if is_valid_line(r)]
    return [list(r) for r in rows]


def find_start(grid):
    """
    find the (row, col) of 'S'
    """
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "S":
                return r, c
    raise ValueError("No start S found")


def count_splits_beam_sim(grid):
    # ind S and start the vertical beam
    _, c = find_start(grid)

    grid[1][c] = "|"

    number_of_splits = 0

    # process from row 2 downwards
    for idx in range(2, len(grid)):
        prev_row = grid[idx - 1]
        cur_row = grid[idx]

        # 1) vertical propagation: copy '|' straight down where there's no '^'
        for j, ch in enumerate(prev_row):
            if ch == "|" and cur_row[j] != "^":
                cur_row[j] = "|"

        # 2) splits: only where a beam hits a '^' from above
        for j, ch in enumerate(cur_row):
            if ch == "^" and prev_row[j] == "|":
                left = j - 1
                right = j + 1

                if left >= 0 and cur_row[left] != "^":
                    cur_row[left] = "|"
                if right < len(cur_row) and cur_row[right] != "^":
                    cur_row[right] = "|"

                if left >= 0 and right < len(cur_row):
                    number_of_splits += 1

    # Build result string
    result = ""
    for row_as_list in grid:
        result += "".join(row_as_list) + "\n"

    return number_of_splits


def count_quantum_timelines(grid):
    R = len(grid)
    C = len(grid[0])

    start_r, start_c = find_start(grid)

    # precompute splitter columns per row
    splitter_cols_by_row = [[] for _ in range(R)]
    for r in range(R):
        row = grid[r]
        cols = []
        for c in range(C):
            if row[c] == "^":
                cols.append(c)
        splitter_cols_by_row[r] = cols

    ways = [0] * C
    ways[start_c] = 1

    finished = 0
    last_col = C - 1

    # process rows below S
    for r in range(start_r + 1, R):
        cols = splitter_cols_by_row[r]
        if not cols:
            # no splitters => ways unchanged
            continue

        # start with "everything goes straight down" (fast C-level copy)
        new = ways.copy()
        w = ways

        # only adjust at splitter columns
        for c in cols:
            amt = w[c]
            if amt == 0:
                continue

            # remove straight-down at the splitter
            new[c] -= amt

            # left branch
            if c > 0:
                new[c - 1] += amt
            else:
                finished += amt

            # right branch
            if c < last_col:
                new[c + 1] += amt
            else:
                finished += amt

        ways = new

    return finished + sum(ways)

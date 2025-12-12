EXAMPLE = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""


def count_neighbors(grid, r, c):
    """
    count how many neighboring cells (out of 8) contain '@'
    around position (r, c).
    """
    rows = len(grid)
    cols = len(grid[0])
    neighbors = 0

    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # skip the cell itself
            if dr == 0 and dc == 0:
                continue

            nr = r + dr
            nc = c + dc

            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == "@":
                    neighbors += 1

    return neighbors


def count_accessible(grid, k=4):
    """
    part 1 helper.

    counts how many paper rolls (@) are accessible by a forklift.

    a roll is accessible if it has fewer than `k` neighboring rolls
    in the 8 surrounding positions.
    """

    rows = len(grid)
    cols = len(grid[0])
    accessible = 0

    # go through every cell in the grid
    for r in range(rows):
        for c in range(cols):
            # skip if it is not a roll of paper
            if grid[r][c] != "@":
                continue

            # check all 8 surrounding cells
            neighbors = count_neighbors(grid, r, c)
            # forklift can access this roll
            if neighbors < k:
                accessible += 1

    return accessible


def remove_all_accessible(grid, k=4):
    """
    part 2 helper.

    repeatedly removes all accessible paper rolls (@),
    until no more can be removed.

    returns the total number of rolls removed.
    """
    rows = len(grid)
    cols = len(grid[0])
    total_removed = 0

    # keep repeating until no more removals
    while True:
        to_remove = []

        # scan the entire grid
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != "@":
                    continue

                # count neighboring rolls
                neighbors = count_neighbors(grid, r, c)
                # mark roll for removal if accessible
                if neighbors < k:
                    to_remove.append((r, c))

        if not to_remove:
            break  # no more changes

        # remove all marked rolls at once
        for r, c in to_remove:
            grid[r][c] = "."

        total_removed += len(to_remove)

    return total_removed

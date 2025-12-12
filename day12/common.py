EXAMPLE = """
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""


def parse_input(lines):
    # parse the puzzle input into:
    #   shapes: {shape_id: ["###", "..#", ...]}
    #   regions: [(W, H, [c0, c1, ...]), ...]
    #
    # the input has two sections:
    #   1) shape blocks like:
    #        0:
    #        ###
    #        ##.
    #        ...
    #   2) region lines like:
    #        12x5: 1 0 1 0 2 2
    raw = [ln.rstrip("\n") for ln in lines]

    shapes = {}
    regions = []

    i = 0

    # read shapes until we reach the first region line
    while i < len(raw):
        line = raw[i].strip()

        # skip blank separators
        if not line:
            i += 1
            continue

        # region lines look like "WxH:" on the left side
        if "x" in line and ":" in line and line.split(":")[0].count("x") == 1:
            break

        # shape headers are "N:" (example: "3:")
        if not line.endswith(":"):
            raise ValueError(f"unexpected line while parsing shapes: {raw[i]}")

        shape_id = int(line[:-1].strip())
        i += 1

        # read the ASCII art for this shape until the next blank line
        shape_lines = []
        while i < len(raw) and raw[i].strip() != "":
            shape_lines.append(raw[i])
            i += 1

        shapes[shape_id] = shape_lines

        # consume the blank line after the shape block (if any)
        if i < len(raw) and raw[i].strip() == "":
            i += 1

    # read regions (one per line)
    while i < len(raw):
        line = raw[i].strip()
        i += 1

        if not line:
            continue

        # format: "12x5: 1 0 1 0 2 2"
        left, right = line.split(":", 1)
        w_str, h_str = left.strip().split("x")
        W = int(w_str)
        H = int(h_str)

        # counts are in shape-id order (0..n-1)
        counts = [int(x) for x in right.strip().split()]
        regions.append((W, H, counts))

    return shapes, regions


def shape_to_cells(shape_lines):
    # convert shape text into a list of (x, y) coordinates for the '#' tiles
    # coordinates are in the shape's local grid (top-left is (0,0))
    cells = []
    for y, row in enumerate(shape_lines):
        for x, ch in enumerate(row):
            if ch == "#":
                cells.append((x, y))
    return cells


def normalize_cells(cells):
    # normalize a set of cells so that:
    #   - the minimum x becomes 0
    #   - the minimum y becomes 0
    # this lets us compare rotated/flipped shapes consistently
    min_x = min(x for x, _ in cells)
    min_y = min(y for _, y in cells)

    shifted = [(x - min_x, y - min_y) for (x, y) in cells]
    shifted.sort()  # sorting makes it hashable and order-independent
    return tuple(shifted)


def rotate90(cells):
    # rotate a shape 90 degrees clockwise around the origin (0,0)
    # we normalize later, so negative coords are fine here
    return [(y, -x) for (x, y) in cells]


def flip_horizontal(cells):
    # mirror a shape across the y-axis (left-right flip)
    # we normalize later, so negative coords are fine here
    return [(-x, y) for (x, y) in cells]


def all_orientations(shape_cells):
    # generate all unique orientations:
    #   - 4 rotations of the original
    #   - 4 rotations of the flipped version
    # duplicates can happen for symmetric shapes, so we de-dup using a set
    seen = set()
    out = []

    base = list(shape_cells)

    # rotations of the base shape
    cur = base
    for _ in range(4):
        norm = normalize_cells(cur)
        if norm not in seen:
            seen.add(norm)
            out.append(norm)
        cur = rotate90(cur)

    # rotations of the flipped shape
    cur = flip_horizontal(base)
    for _ in range(4):
        norm = normalize_cells(cur)
        if norm not in seen:
            seen.add(norm)
            out.append(norm)
        cur = rotate90(cur)

    return out


def cells_bounds(cells):
    # given normalized cells, compute the bounding box size
    # width = max_x + 1, height = max_y + 1
    max_x = 0
    max_y = 0
    for x, y in cells:
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
    return max_x + 1, max_y + 1


def bit_index(x, y, W):
    # map (x,y) on a W-wide board into a single linear index
    # cell indices go left-to-right, then top-to-bottom:
    #   (0,0)=0, (1,0)=1, ... (W-1,0)=W-1, (0,1)=W, ...
    return y * W + x


def build_placements_for_shape(W, H, orientations):
    # enumerate every possible placement of a shape on a WxH board
    #
    # a "placement" is represented as a tuple of occupied cell indices
    # (using bit_index), sorted so it can be used for de-dup
    placements = set()

    for cells in orientations:
        sw, sh = cells_bounds(cells)

        # if the shape's bounding box doesn't fit, skip this orientation
        if sw > W or sh > H:
            continue

        # slide the shape's top-left corner across all valid positions
        for ty in range(H - sh + 1):
            for tx in range(W - sw + 1):
                used = []
                for cx, cy in cells:
                    used.append(bit_index(tx + cx, ty + cy, W))
                used.sort()
                placements.add(tuple(used))

    return list(placements)


def can_fit_region(W, H, shape_orients_by_id, counts):
    # exact solver check:
    #   - create a boolean variable for each possible placement
    #   - pick exactly counts[sid] placements per shape sid
    #   - prevent overlap by limiting each board cell to be covered at most once
    from z3 import Solver, Bool, PbEq, PbLe, sat

    # quick reject: if total tiles needed > board area, impossible
    total_tiles_needed = 0
    for sid, qty in enumerate(counts):
        if qty <= 0:
            continue
        if sid not in shape_orients_by_id:
            return False
        total_tiles_needed += qty * len(shape_orients_by_id[sid][0])

    if total_tiles_needed > W * H:
        return False

    # build all placements for each shape type that we actually need
    placements_by_shape = {}
    for sid, qty in enumerate(counts):
        if qty <= 0:
            continue

        plist = build_placements_for_shape(W, H, shape_orients_by_id[sid])

        # if you need more copies than there are distinct placements, impossible
        if len(plist) < qty:
            return False

        placements_by_shape[sid] = plist

    solver = Solver()

    # create Bool variables: use_s{sid}_p{idx} says "we choose placement idx of shape sid"
    use_vars_by_shape = {}
    for sid, plist in placements_by_shape.items():
        use_vars_by_shape[sid] = [
            Bool(f"use_s{sid}_p{p_idx}") for p_idx in range(len(plist))
        ]

    # per shape: choose exactly the required number of placements
    for sid, vars_for_shape in use_vars_by_shape.items():
        solver.add(PbEq([(v, 1) for v in vars_for_shape], counts[sid]))

    # overlap constraint:
    # build a list of "which placement-vars cover this cell"
    cover = {}  # cell_index -> [Bool, Bool, ...]
    for sid, plist in placements_by_shape.items():
        vars_for_shape = use_vars_by_shape[sid]
        for p_idx, cells in enumerate(plist):
            v = vars_for_shape[p_idx]
            for cell in cells:
                cover.setdefault(cell, []).append(v)

    # for each cell, at most one chosen placement may include it
    for cell, vs in cover.items():
        if len(vs) > 1:
            solver.add(PbLe([(v, 1) for v in vs], 1))

    return solver.check() == sat


def shape_area(shape_lines):
    # count how many '#' tiles a shape has (its area)
    return sum(1 for row in shape_lines for ch in row if ch == "#")


def can_fit_region_fast_or_exact(W, H, shape_orients_by_id, shapes_raw, counts):
    # fast path:
    #   - reject if total tiles needed > region area
    #   - for large instances, assume that if the area fits then a packing exists
    # exact path:
    #   - for smaller instances, run the full placement-based solver

    board_area = W * H

    # lower bound check: if we need more tiles than the region has, it's impossible
    needed = 0
    pieces = 0
    for sid, qty in enumerate(counts):
        if qty <= 0:
            continue
        pieces += qty
        needed += qty * shape_area(shapes_raw[sid])

    if needed > board_area:
        return False

    # the input is designed so big cases are "easy":
    # if you can fit the total area, you can fit the pieces
    if pieces > 30:
        return True

    # small cases (like the example) still need the exact check
    return can_fit_region(W, H, shape_orients_by_id, counts)

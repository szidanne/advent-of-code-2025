from collections import deque

EXAMPLE = """
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""


def is_valid_line(s):
    return s is not None and s != ""


def read_points(lines):
    """
    reads lines like "x,y" into a list of (x, y) ints.
    keeps input order (important for Part 2).
    """
    pts = []
    for line in lines:
        line = line.strip()
        if not is_valid_line(line):
            continue
        parts = line.split(",")
        x = int(parts[0])
        y = int(parts[1])
        pts.append((x, y))
    return pts


def rectangle_area_inclusive(x1, y1, x2, y2):
    """
    inclusive tile count:
    if corners are (x1,y1) and (x2,y2),
    width in tiles  = abs(x1-x2)+1
    height in tiles = abs(y1-y2)+1
    """
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)

    return (dx + 1) * (dy + 1)


# part 1 helpers (simple brute force)


def max_area_any_red(points):
    """
    part 1:
    try every pair of red tiles as opposite corners.
    return maximum inclusive area.
    """
    n = len(points)
    best = 0

    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            area = rectangle_area_inclusive(x1, y1, x2, y2)
            if area > best:
                best = area

    return best


# part 2 helpers


def _make_boundaries(values):
    """
    build coordinate boundaries for compression.

    we treat each tile coordinate v as covering interval [v, v+1).
    so we must include v and v+1 as boundary values.

    example: if tiles exist at x=2..11, the x-interval is [2, 12).
    """
    bounds = set()
    for v in values:
        bounds.add(v)
        bounds.add(v + 1)
    return bounds


def _build_prefix_sum(weight_grid):
    """
    2D prefix sum over a grid of non-negative integers.
    weight_grid is indexed as [y][x].

    returns ps with shape (H+1) x (W+1) where:
      ps[y+1][x+1] = sum of weight_grid[0..y][0..x]
    """
    H = len(weight_grid)
    W = len(weight_grid[0])

    ps = []
    for _ in range(H + 1):
        ps.append([0] * (W + 1))

    for y in range(H):
        row_sum = 0
        for x in range(W):
            row_sum += weight_grid[y][x]
            ps[y + 1][x + 1] = ps[y][x + 1] + row_sum

    return ps


def _rect_sum(ps, x0, x1, y0, y1):
    """
    Sum over rectangle in compressed CELL coordinates:
      x in [x0, x1)
      y in [y0, y1)
    """
    return ps[y1][x1] - ps[y0][x1] - ps[y1][x0] + ps[y0][x0]


def _compress_loop_region(red_points_in_order):
    """
    build an "allowed region" (red boundary + green boundary + green interior)
    using coordinate compression.

    returns:
      x_index: dict boundary_x -> boundary index
      y_index: dict boundary_y -> boundary index
      ps_allowed: prefix sum of allowed tile counts per compressed cell
    """
    # Collect all x and y values from vertices
    xs = []
    ys = []
    for x, y in red_points_in_order:
        xs.append(x)
        ys.append(y)

    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)

    # add padding so (outside) flood fill has space around the loop.
    # we add one tile margin around the bounding box.
    pad_x0 = min_x - 1
    pad_x1 = max_x + 2
    pad_y0 = min_y - 1
    pad_y1 = max_y + 2

    # build boundary sets for compression
    x_bounds = _make_boundaries(xs)
    y_bounds = _make_boundaries(ys)

    # include padding boundaries (and their +1 implicitly)
    x_bounds.add(pad_x0)
    x_bounds.add(pad_x0 + 1)
    x_bounds.add(pad_x1)
    x_bounds.add(pad_x1 + 1)

    y_bounds.add(pad_y0)
    y_bounds.add(pad_y0 + 1)
    y_bounds.add(pad_y1)
    y_bounds.add(pad_y1 + 1)

    # sort boundary coordinates
    x_vals = sorted(x_bounds)
    y_vals = sorted(y_bounds)

    # map boundary coordinate -> index
    x_index = {}
    for i, v in enumerate(x_vals):
        x_index[v] = i

    y_index = {}
    for i, v in enumerate(y_vals):
        y_index[v] = i

    # number of compressed cells is (len(boundaries)-1)
    W = len(x_vals) - 1
    H = len(y_vals) - 1

    # each cell represents a block of tiles:
    # x width = x_vals[i+1] - x_vals[i]
    # y height = y_vals[j+1] - y_vals[j]
    x_width = []
    for i in range(W):
        x_width.append(x_vals[i + 1] - x_vals[i])

    y_height = []
    for j in range(H):
        y_height.append(y_vals[j + 1] - y_vals[j])

    # mark boundary cells (red + green loop) as "blocked" for outside flood fill.
    boundary = []
    for _ in range(H):
        boundary.append([False] * W)

    # walk segments between consecutive red points (wrap around).
    n = len(red_points_in_order)
    for k in range(n):
        x1, y1 = red_points_in_order[k]
        x2, y2 = red_points_in_order[(k + 1) % n]

        if x1 == x2:
            # vertical segment: x fixed, y ranges
            x = x1
            y_low = y1
            y_high = y2
            if y_low > y_high:
                y_low, y_high = y_high, y_low

            # tile y range inclusive => boundary y interval [y_low, y_high+1)
            ix0 = x_index[x]
            ix1 = x_index[x + 1]
            iy0 = y_index[y_low]
            iy1 = y_index[y_high + 1]

            # mark all cells that intersect that 1-tile-wide column range
            # ix0..ix1-1 is exactly 1 cell wide (because x and x+1 are in boundaries)
            for yy in range(iy0, iy1):
                boundary[yy][ix0] = True

        else:
            # horizontal segment: y fixed, x ranges
            y = y1
            x_low = x1
            x_high = x2
            if x_low > x_high:
                x_low, x_high = x_high, x_low

            # tile x range inclusive => boundary x interval [x_low, x_high+1)
            ix0 = x_index[x_low]
            ix1 = x_index[x_high + 1]
            iy0 = y_index[y]
            iy1 = y_index[y + 1]

            for xx in range(ix0, ix1):
                boundary[iy0][xx] = True

    # flood fill outside in compressed cell grid (4-neighbor)
    outside = []
    for _ in range(H):
        outside.append([False] * W)

    q = deque()

    # start from a guaranteed outside cell: near padding corner
    # use the cell containing tile (pad_x0, pad_y0)
    start_x = x_index[pad_x0]
    start_y = y_index[pad_y0]

    # start_x/start_y are boundary indices; cell indices are same here
    if 0 <= start_x < W and 0 <= start_y < H and not boundary[start_y][start_x]:
        outside[start_y][start_x] = True
        q.append((start_x, start_y))

    while q:
        cx, cy = q.popleft()

        # 4 neighbors
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx = cx + dx
            ny = cy + dy

            if nx < 0 or nx >= W or ny < 0 or ny >= H:
                continue
            if outside[ny][nx]:
                continue
            if boundary[ny][nx]:
                continue

            outside[ny][nx] = True
            q.append((nx, ny))

    # build allowed weight grid:
    # allowed = boundary OR (not outside)
    allowed_weight = []
    for y in range(H):
        row = []
        for x in range(W):
            is_allowed = boundary[y][x] or (not outside[y][x])
            if is_allowed:
                row.append(x_width[x] * y_height[y])  # number of tiles in this block
            else:
                row.append(0)
        allowed_weight.append(row)

    ps_allowed = _build_prefix_sum(allowed_weight)

    return x_index, y_index, ps_allowed


def max_area_red_corners_inside_loop(red_points_in_order):
    """
    part 2:
    find max rectangle area with opposite corners being red tiles,
    and the entire rectangle must be within the red+green region.

    we:
    - build prefix sum of allowed region by compression + flood fill
    - check each pair of red points as corners
    """
    x_index, y_index, ps_allowed = _compress_loop_region(red_points_in_order)

    n = len(red_points_in_order)
    best = 0

    for i in range(n):
        x1, y1 = red_points_in_order[i]
        for j in range(i + 1, n):
            x2, y2 = red_points_in_order[j]

            # rectangle bounds (inclusive in tile coordinates)
            xmin = x1
            xmax = x2
            if xmin > xmax:
                xmin, xmax = xmax, xmin

            ymin = y1
            ymax = y2
            if ymin > ymax:
                ymin, ymax = ymax, ymin

            # expected tile count
            expected = (xmax - xmin + 1) * (ymax - ymin + 1)

            # compressed cell rectangle uses boundaries:
            # tiles x in [xmin, xmax] => boundary interval [xmin, xmax+1)
            # tiles y in [ymin, ymax] => boundary interval [ymin, ymax+1)
            ix0 = x_index[xmin]
            ix1 = x_index[xmax + 1]
            iy0 = y_index[ymin]
            iy1 = y_index[ymax + 1]

            allowed = _rect_sum(ps_allowed, ix0, ix1, iy0, iy1)

            if allowed == expected:
                if expected > best:
                    best = expected

    return best

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aoc_common import parse_example, read_input
from day12.common import (
    EXAMPLE,
    parse_input,
    shape_to_cells,
    all_orientations,
    can_fit_region_fast_or_exact,
)


def build_shape_orientations(shapes_raw):
    """
    shapes_raw: dict[sid] -> list[str]
    returns: dict[sid] -> list[normalized cell-tuples] (unique orientations)
    """
    out = {}
    for sid, lines in shapes_raw.items():
        base_cells = shape_to_cells(lines)
        out[sid] = all_orientations(base_cells)
    return out


def solve(lines):
    shapes_raw, regions = parse_input(lines)
    shape_orients_by_id = build_shape_orientations(shapes_raw)

    ok = 0
    for W, H, counts in regions:
        if can_fit_region_fast_or_exact(W, H, shape_orients_by_id, shapes_raw, counts):
            ok += 1
    return ok


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "example":
        data = parse_example(EXAMPLE)
    else:
        data = read_input()

    print(solve(data))

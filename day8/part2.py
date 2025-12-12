import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aoc_common import parse_example, read_input
from day8.common import EXAMPLE, read_points, build_all_edges, UnionFind


def solve(lines):
    points = read_points(lines)
    edges = build_all_edges(points)

    uf = UnionFind(len(points))

    last_i = None
    last_j = None

    for _, i, j in edges:
        merged = uf.union(i, j)
        if merged:
            last_i = i
            last_j = j

            if uf.components == 1:
                break

    x1 = points[last_i][0]
    x2 = points[last_j][0]
    return x1 * x2


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "example":
        data = parse_example(EXAMPLE)
    else:
        data = read_input()

    print(solve(data))

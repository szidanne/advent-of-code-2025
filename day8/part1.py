import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aoc_common import parse_example, read_input
from day8.common import EXAMPLE, read_points, build_all_edges, UnionFind


def solve(lines, k):
    points = read_points(lines)
    edges = build_all_edges(points)

    uf = UnionFind(len(points))

    # take the first k edges in the sorted list, even if some do nothing.
    if k > len(edges):
        k = len(edges)

    for idx in range(k):
        _, i, j = edges[idx]
        uf.union(i, j)  # if already same component, it does nothing

    sizes = uf.component_sizes()
    sizes.sort(reverse=True)

    # multiply the three largest component sizes
    # (assume there are at least 3 components; if not, multiply whatever exists)
    result = 1
    take = 3
    if take > len(sizes):
        take = len(sizes)

    for k in range(take):
        result *= sizes[k]

    return result


if __name__ == "__main__":
    k = 1000
    if len(sys.argv) > 1 and sys.argv[1] == "example":
        k = 10
        data = parse_example(EXAMPLE)
    else:
        data = read_input()

    print(solve(data, k))

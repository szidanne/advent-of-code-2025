import sys

from pathlib import Path

# --- add repo root to sys.path so we can import aoc_common.py ---
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aoc_common import parse_example, read_input
from common import build_graph, dfs_all
from day11.common import EXAMPLE


def main():
    # example override
    if len(sys.argv) > 1 and sys.argv[1] == "example":
        data = parse_example(EXAMPLE)
    else:
        data = read_input()

    graph = build_graph(data)
    total_paths = dfs_all(graph, "you", "out", memo={})
    print(total_paths)


if __name__ == "__main__":
    main()

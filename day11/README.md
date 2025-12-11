# Advent of Code 2025 — Day 11  
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![AoC](https://img.shields.io/badge/Advent%20of%20Code-2025-red.svg)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)

Solutions for **Day 11** of Advent of Code 2025.  
This puzzle involves traversing a directed acyclic graph to count possible paths from `you/svr` → `out`.

Data flows forward only along edges. The tasks are:
- **Part 1:** Count all distinct paths from you to out.
- **Part 2:** Count all distinct paths from svr to out, and among them, how many visit a required set of devices (e.g. `{dac, fft}`).

## Structure

```text
day11/
│── common.py   # shared helpers (graph parsing + DFS solvers)
│── part1.py    # Part 1: count all paths from start → out
│── part2.py    # Part 2: count paths that must include specific nodes
└── README.md
```

## Running

### Part 1

Count all paths from `you` → `out`.

#### ASCII Diagram — How the Reactor Network Is Traversed

Below is a conceptual visualization of the device graph:

```text

                (start)
                  you
                 /   \
                /     \
              bbb     ccc
             /  \    / | \
            /    \  /  |  \
         ddd    eee    |   fff
          |      |     |    |
         ggg    out   out   out
          |
         out
```

*What the diagram shows*
- Each node is a device.
- Edges are one-way flows (data only travels forward).
- `you` is always the entry point.
- `out` is the reactor output and the final destination.
- Paths branch forward but never backward.

### Run Part 1

#### Reads input from STDIN:

`python3 part1.py < input.txt`

#### Run the built-in example:

`python3 part1.py example`


### Part 2

Count both:

- total *paths*, and
- *paths that visit a required set of nodes* (e.g., `{dac, fft}`)

Some puzzles include extra devices that merge or diverge in more complex ways.
Here’s a version showing a multi-branch DAG like in Part 2:

#### Counts **all** paths and **valid** paths (those visiting required nodes):

### Run Part 2

#### Reads input from STDIN:

`python3 part2.py < input.txt`

#### Example mode:

`python3 part2.py example`


## Notes

- `common.py` implements graph parsing and two DFS-based solvers:
  - `dfs_all`: count all paths from `start` to `end`
  - `dfs_required`: count only paths that visit all required nodes
- Memoization ensures efficient computation without enumerating every raw path.

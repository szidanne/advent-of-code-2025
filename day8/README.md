# Advent of Code 2025 — Day 8  
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![AoC](https://img.shields.io/badge/Advent%20of%20Code-2025-red.svg)](https://adventofcode.com/2025/day/8)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)

Solutions for **Day 8** of Advent of Code 2025.

This puzzle is about connecting **3D junction boxes** using the **shortest connections first**, while tracking which boxes end up in the same electrical circuit.

---

## Problem Summary

You are given a list of junction box positions in **3D space**, one per line:

```text
x,y,z
x,y,z
...
```

Two boxes can be connected with a string of lights, and electricity can flow along connections.
That means connections create circuits (connected components).

Connections are attempted in increasing order of straight-line distance:

- Find the closest pair, connect them
- Then the next closest pair, connect them
- If two boxes are already in the same circuit, connecting them does nothing

---

## Structure

```text
day8/
│── common.py   # parsing, distance, edge sorting, union-find
│── part1.py    # Part 1: after K shortest attempts, multiply 3 largest circuits
│── part2.py    # Part 2: connect until 1 circuit, multiply X coords of last merge
└── README.md
```

---

## Core Idea (Both Parts)

### Step 1: Build all possible connections (pairs)

If there are `N` junction boxes, there are:

```text
N * (N - 1) / 2
```

possible pairs.

Each pair is an “edge” between junction boxes `i` and `j`.

### Step 2: Sort edges by distance

We sort by **squared distance** (no floating point needed):

```text
d^2 = (dx*dx) + (dy*dy) + (dz*dz)
```

Sorting by `d^2` gives the same ordering as sorting by `d`.

### Step 3: Process edges using Union-Find

Union-Find (Disjoint Set Union) tracks which nodes are already connected.

---

## Visualizations

### “Circuits” as components

Start: each junction box is its own circuit.

```text
(0)  (1)  (2)  (3)  (4)
```

Connect the closest pair (say 1 and 3):

```text
(0)  (1)----(3)  (2)  (4)
```

Now circuit sizes are:

```text
{1,3} size 2
{0}   size 1
{2}   size 1
{4}   size 1
```

If we later try to connect 1 and 3 again, nothing changes:

```text
(1)----(3)   (already same circuit, so union does nothing)
```

### Union-Find mental model

Think of each circuit having a “leader”:

```text
leader(1) = 1
leader(3) = 1  (after union)
```

If two nodes have the same leader, they are already connected.

---

## Part 1 — After 1000 Closest Connection Attempts

### Rules

-   Attempt to connect the **1000 closest pairs** (sorted by distance)
-   Even if a pair is already connected, it still counts as an “attempt”
-   After those attempts, compute the sizes of all circuits
-   Multiply the sizes of the **three largest circuits**

### Example explanation

In the sample text, after the **10** shortest connection attempts, the circuit sizes include:

```text
5, 4, 2, 2, 1, 1, 1, 1, 1, 1, 1
```

The three largest are `5, 4, 2`:

```text
5 * 4 * 2 = 40
```

---

## Part 2 — Connect Until Everything Is One Circuit

### Rules

-   Keep attempting connections in sorted order
-   Only stop when all junction boxes are in **one** circuit
-   Track the **last connection that actually merged two circuits**
-   Multiply the **X coordinates** of those two junction boxes

### “Last merge” idea

Before the final merge:

```text
Circuit A: ( ... )
Circuit B: ( ... )
```

Final connection merges them:

```text
Circuit A ---- Circuit B   =>   one big circuit
```

We take the last merged edge `(i, j)` and return:

```text
x[i] * x[j]
```

---

## Run Part 1

#### Reads input from STDIN:

`python3 part1.py < input.txt`

#### Run the built-in example:

`python3 part1.py example`

---

## Run Part 2

#### Reads input from STDIN:

`python3 part2.py < input.txt`

#### Run the built-in example:

`python3 part2.py example`

---

## Notes

-   `common.py` contains:
    -   input parsing (`read_points`)
    -   distance calculation (`squared_distance`)
    -   edge generation + sorting (`build_all_edges`)
    -   union-find (`UnionFind`)

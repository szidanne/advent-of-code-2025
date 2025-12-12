# Advent of Code 2025 — Day 7
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![AoC](https://img.shields.io/badge/Advent%20of%20Code-2025-red.svg)](https://adventofcode.com/2025/day/7)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)

Solutions for **Day 7** of Advent of Code 2025.

This puzzle is about simulating a **tachyon beam** moving through a grid of splitters, then upgrading the model to a **quantum version** where one particle explores all possible paths (with merges).

---

## Problem Summary

You are given a **grid of characters** containing:

-   `S` = the start point
-   `^` = a splitter
-   `.` (or anything else) = empty space

A particle starts at `S` and moves **downward** row by row.

When a particle reaches a splitter `^`:
-   the particle does **not** continue straight down
-   it instead splits into **left** and **right** branches (one column left / one column right) on the next row
    

If a branch moves off the left or right edge, that timeline ends.

---

## Structure

```text
day7/
│── common.py   # grid parsing, helpers, beam logic
│── part1.py    # Part 1: count split events (classic simulation)
│── part2.py    # Part 2: count quantum timelines (DP with merges)
└── README.md
```

---

## Part 1 — Count Split Events

### Rules

-   Start at `S`
    
-   Move downward row by row
    
-   A split event happens when a vertical beam reaches a `^`
    
-   That event emits two sideways beams (left and right) on the same row
    
-   Count **split events**, not beams
    

### Visual idea

A vertical beam reaches a splitter:

```text
   S
   |
  |^|
  | |
```

The splitter “consumes” the beam from above and emits left/right.

---

## Part 2 — Count Quantum Timelines

### New Rules

Now it’s a **quantum tachyon manifold**:

-   Only one particle is sent in
-   At each splitter, the particle takes **both** left and right paths
-   We use the many-worlds interpretation:
    -   each splitter causes a **timeline split** 
    -   different histories can still end up in the **same place** (merging)
        

So the answer is:

> The total number of timelines active after the particle completes all possible journeys.

### Efficient approach (DP by column)

We keep:

```text
ways[c] = number of timelines currently at column c
```

Then process row by row:

-   If below is not `^`: timelines stay in the same column
-   If below is `^`: timelines move to `c-1` and `c+1`
-   Timelines that go off-grid are counted as finished
    

To make this fast in Python:

-   Precompute which rows contain `^`
-   Skip rows with no `^` (they don’t change anything)
-   Update only using the splitter positions for that row
    

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
    -   grid parsing (`read_grid`) 
    -   locating the start (`find_start`) 
    -   Part 1 classic simulation (`count_splits_beam_sim`)
    -   Part 2 quantum DP (`count_quantum_timelines`)
-   Part 1 is a direct beam simulation
-   Part 2 is dynamic programming that supports timeline merges
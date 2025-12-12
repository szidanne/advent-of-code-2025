# Advent of Code 2025 — Day 12
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![AoC](https://img.shields.io/badge/Advent%20of%20Code-2025-red.svg)](https://adventofcode.com/2025/day/11)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)

Solutions for **Day 12** of Advent of Code 2025.

This puzzle is about checking whether a set of polyomino-like present shapes can fit into rectangular regions on a grid **without overlap**, where each shape may be **rotated** or **flipped**.

---

## Problem Summary

The input has two sections:

1) **present shapes** (indexed)  
2) **regions** to test, each with a size and required counts of each shape

Example:

```text
0:
###
##.
##.

1:
###
##.
.##

...

12x5: 1 0 1 0 2 2
```

-   `#` means occupied cell
-   `.` means empty cell
-   a region line `12x5: 1 0 1 0 2 2` means:
    -   width = 12, height = 5
    ```text
    ............
    ............
    ............
    ............
    ............
    ```
    -   need 1 of shape 0, 0 of shape 1, 1 of shape 2, 0 of shape 3, 2 of shape 4, 2 of shape 5

Goal: **count how many regions can fit all required presents**.

---

## Structure

```text
day12/
│── common.py    # parsing helpers + shared utilities
│── part1.py     # solution runner (single part)
└── README.md
```

---

## Key Observations

### Shapes are on a grid

Each present is a set of grid cells (the `#` positions).  
When placing a shape, we choose:

-   an orientation (rotation/flip)
-   a top-left placement offset `(tx, ty)` inside the region

### Overlap is forbidden

Two shapes cannot occupy the same grid cell.

### General packing is hard

Trying to solve *every* region by explicit placement search is a packing problem and is computationally expensive.

The input is constructed so a **very simple test** is enough to determine if a region is impossible.

---

## Part 1 — Simple “impossible” check

### Rule used

A region **cannot** fit the required presents if:

```text
(total number of occupied cells needed) > (region area)
```

That is:

```text
sum(count[s] * area(shape s)) > (W * H)
```

Where:

-   `area(shape s)` = number of `#` cells in shape `s`
-   `W * H` = total grid cells in the region

If the total required occupied cells exceed the board area, overlap is unavoidable, so the region is impossible.

### Why this is so fast

For each region:

-   compute `W * H`
-   compute one weighted sum over 6 shapes
-   compare

That’s it. No placement enumeration, no search, no solver.

### Important limitation

This check is **only a necessary condition**, not sufficient in general:

-   even if the total area fits, shapes might still not pack.

For this specific AoC input, the construction ensures the above test is enough to correctly decide which regions fail.

---

## Implementation Outline

### 1) Parse shapes

Each shape is read as a small `#`/`.` grid, and we precompute:

```text
shape_area[s] = number of '#'
```

### 2) Parse regions

Each region gives `(W, H, counts[0..5])`.

### 3) Evaluate each region

Compute:

```text
needed = Σ counts[s] * shape_area[s]
capacity = W * H
```

If `needed > capacity`, region is impossible.  
Otherwise, count it as possible (per input guarantees).

---

## Run

Reads input from STDIN:

```bash
python3 part1.py < input.txt
```

---

## Notes

-   this solution intentionally avoids brute-force packing
-   rotations/flips don’t matter for the area test (they preserve `#` count)
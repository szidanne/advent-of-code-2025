# Advent of Code 2025 — Day 9  
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![AoC](https://img.shields.io/badge/Advent%20of%20Code-2025-red.svg)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)

Solutions for **Day 9** of Advent of Code 2025.

This puzzle is about finding the **largest axis-aligned rectangle** whose **opposite corners are red tiles**.

Part 2 adds a “playable area” constraint: the rectangle must be fully inside the **red+green region** formed by a loop.

---

## Problem Summary

Input is a list of **red tile coordinates**:

```text
x,y
x,y
...
```

-   Tiles are on an infinite grid.
    
-   A rectangle is axis-aligned.
    
-   You may choose **any two red tiles** as opposite corners.
    

Tile area is counted **in tiles**, inclusively:

```text
area = (abs(x1-x2) + 1) * (abs(y1-y2) + 1)
```

---

## Structure

```text
day9/
│── common.py   # parsing + shared rectangle / region logic
│── part1.py    # Part 1: largest rectangle using any two red corners
│── part2.py    # Part 2: largest rectangle fully inside the loop region
└── README.md
```

---

## Part 1 — Largest Rectangle With Red Corners

### Rules

-   Pick any two red tiles as opposite corners.
-   Rectangle can include any tiles (no restrictions).
-   Find the maximum area.

### Approach

Brute-force all pairs of red points:

```text
for each i < j:
    compute area using inclusive formula
    keep the maximum
```

This directly matches the rule “any two red tiles can be opposite corners”.

### visualization (corners only)

```text
y
^
|      #.........
|      .....#....
|      ..........
|      #........#
+------------------> x
```

Pick two `#` as opposite corners → area is width×height in tiles.

---

## Part 2 — Rectangle Must Use Only Red/Green Tiles

### New Rules

The input list is now ordered:

-   Each red tile is connected to the **previous** and **next** red tile
-   The connection is a straight orthogonal line (same x or same y)
-   All tiles along those segments become **green**
-   The loop wraps: last connects to first
-   Every tile **inside the loop** is also green

Your rectangle must still have **red corners**, but every tile inside the rectangle  
must be **red or green** (i.e., inside the loop region).

### boundary + interior

Red points define a loop (boundary is red+green):

```text
..............
.......#XXX#..
.......X...X..
..#XXXX#...X..
..X........X..
..#XXXXXX#.X..
.........X.X..
.........#X#..
..............
```

Inside the loop is also green (filled area).

### Why this is harder

Coordinates can be huge, so we can’t build a real 2D grid of the whole theater floor.

We need a way to:

-   represent the loop region compactly
-   test whether a candidate rectangle is fully inside it

---

## Part 2 Approach (Compression + Flood Fill + Prefix Sum)

### 1) Coordinate compression

We only care about x/y values that matter:

-   red vertices’ x and y
-   also `x+1` and `y+1` (tile boundaries)
-   plus a small padding border so “outside” exists

This creates a much smaller grid of **blocks**.

Each compressed cell represents a block of many tiles:

```text
real tiles:
x in [x_vals[i], x_vals[i+1])
y in [y_vals[j], y_vals[j+1])
```

### 2) Mark the boundary (red+green segments)

For every consecutive pair of red points, mark all compressed cells crossed by the segment as boundary.

### 3) Flood fill outside

We BFS from a guaranteed outside cell (in the padding) and mark all reachable cells that are not blocked by the boundary.

Everything not reachable is inside (green) or boundary (red/green).

### 4) Weighted prefix sum for fast rectangle checks

Each compressed cell has a tile count:

```text
cell_tiles = cell_width * cell_height
```

We build a prefix sum over “allowed tiles” (inside or boundary).

Then for any rectangle (in tile coordinates), we can compute:

-   `expected_area` (inclusive tiles)
-   `allowed_area` from prefix sum

If:

```text
allowed_area == expected_area
```

then every tile in the rectangle is red/green, so the rectangle is valid.

### Outside vs inside idea

```text
outside flood fill starts here:

+--------------------+
| OOOOOOOOOOOOOOOOOO |
| O   ##########   O |
| O   # inside #   O |
| O   ##########   O |
| OOOOOOOOOOOOOOOOOO |
+--------------------+

O = outside cells (reachable)
# = boundary
inside = not reachable (green interior)
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
    -   Part 1 brute force (`max_area_any_red`)
    -   Part 2 loop region building:
        -   coordinate compression
        -   boundary marking
        -   outside flood fill
        -   weighted prefix sums 
    -   Part 2 rectangle search (`max_area_red_corners_inside_loop`) 
-   Part 1 is `O(N^2)` over red points.
-   Part 2 still checks red-corner pairs (`O(N^2)`), but rectangle validation is `O(1)` via prefix sums.
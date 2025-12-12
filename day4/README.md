# Advent of Code 2025 — Day 4  
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![AoC](https://img.shields.io/badge/Advent%20of%20Code-2025-red.svg)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)

Solutions for **Day 4** of Advent of Code 2025.

This puzzle takes place in the **Printing Department**, where rolls of paper are arranged in a grid.  
Each roll (`@`) may or may not be accessible by a forklift depending on how crowded it is.

---

## Problem Summary

Each cell in the grid is either:

- `@` → a roll of paper  
- `.` → empty space  

A forklift can access a roll **only if fewer than 4 of the 8 surrounding cells** also contain rolls.

Adjacency includes **diagonals**.

---

## Structure

```text
day4/
│── common.py   # grid helpers and logic
│── part1.py    # Part 1: count accessible rolls
│── part2.py    # Part 2: repeatedly remove accessible rolls
└── README.md
```

## Part 1 — Count Accessible Rolls

### Goal

Count how many paper rolls can be accessed without removing any rolls.

### Example

Input grid:

- `@` = roll
- `.` = empty
- `x` = roll being removed

```text
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
```

A roll is accessible if less than `4` of its `8` neighbors are also rolls.

#### Accessible rolls are marked with x:

```text
..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.
```

`13` rolls are accessible.

---

## Part 2 — Remove Everything Possible

### Goal

Once a roll is accessible:

- it can be removed
- removing it may expose new _accessible_ rolls
- repeat until nothing more can be removed

#### Process Visualization

- `@` = roll
- `.` = empty
- `x` = roll being removed

Each round removes all currently accessible rolls, then recalculates.

```text
Initial state:
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.

Remove 13 rolls of paper:
..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.

Remove 12 rolls of paper:
.......x..
.@@.x.x.@x
x@@@@...@@
x.@@@@..x.
.@.@@@@.x.
.x@@@@@@.x
.x.@.@.@@@
..@@@.@@@@
.x@@@@@@@.
....@@@...

Remove 7 rolls of paper:
..........
.x@.....x.
.@@@@...xx
..@@@@....
.x.@@@@...
..@@@@@@..
...@.@.@@x
..@@@.@@@@
..x@@@@@@.
....@@@...

Remove 5 rolls of paper:
..........
..x.......
.x@@@.....
..@@@@....
...@@@@...
..x@@@@@..
...@.@.@@.
..x@@.@@@x
...@@@@@@.
....@@@...

Remove 2 rolls of paper:
..........
..........
..x@@.....
..@@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@x.
....@@@...

Remove 1 roll of paper:
..........
..........
...@@.....
..x@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
...x@.....
...@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
....x.....
...@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
..........
...x@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...
```

In the example, `43` rolls can be removed in total.

---

## Run Part 1

#### Reads input from STDIN:

`python3 part1.py < input.txt`

#### Run the built-in example:

`python3 part1.py example`

## Run Part 2

#### Reads input from STDIN:

`python3 part2.py < input.txt`

#### Run the built-in example:

`python3 part2.py example`

---

## How the Solution Works

### Counting neighbors

For each `@`:

- look at all 8 surrounding cells
- count how many are also `@`
- if that number `is < 4`, it’s accessible

### Part 2 loop

```text
while we can remove rolls:
    find all accessible rolls
    remove them
    count how many we removed
```

## Notes

- `common.py` contains:
  - neighbor counting
  - accessibility logic
  - repeated removal loop
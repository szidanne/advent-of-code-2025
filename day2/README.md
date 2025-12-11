# Advent of Code 2025 — Day 2  
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![AoC](https://img.shields.io/badge/Advent%20of%20Code-2025-red.svg)](https://adventofcode.com/2025/day/1)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)

Solutions for **Day 2** of Advent of Code 2025.  
This puzzle involves scanning numeric ID ranges and detecting which IDs consist entirely of repeated digit-sequences.

Two tasks:

- **Part 1:** IDs that are made of a repeated sequence **exactly twice**  
- **Part 2:** IDs that are made of a repeated sequence **two or more times**

All invalid IDs found across all ranges must be **summed**.

---

## Structure

```text
day2/
│── common.py   # shared helpers (range parsing + repeated-pattern detection)
│── part1.py    # part 1: IDs repeated exactly twice
│── part2.py    # part 2: IDs repeated 2+ times
└── README.md
```

---

## Problem Summary

Input consists of comma-separated number ranges like:

```text
11-22,95-115,998-1012,...
```

A range `A-B` means:
Inspect all integers from A through B inclusive.

### What counts as an invalid ID?

## Part 1 — Repeat Exactly Twice

Examples: `55` `6464` `78697869`

These get added to the sum.

### Run Part 1

#### Reads input from STDIN:

`python3 part1.py < input.txt`

#### Run the built-in example:

`python3 part1.py example`

## Part 2 — Repeat Two or More Times

Examples: `12341234` `123123123` `1212121212`

These get added to the sum.

### Run Part 2

#### Reads input from STDIN:

`python3 part2.py < input.txt`

#### Run the built-in example:

`python3 part2.py example`

## Notes

- `common.py` handles:
 - parsing all ranges
 - checking whether a number is fully composed of repeated digit-sequences 
- Part 1 and Part 2 reuse the same detection logic but differ in strictness:
  - Part 1 → exactly 2 repeats
  - Part 2 → ≥ 2 repeats 
- The solvers iterate through each range and sum all IDs flagged as invalid.
# Advent of Code 2025 — Day 5  
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![AoC](https://img.shields.io/badge/Advent%20of%20Code-2025-red.svg)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)

Solutions for **Day 5** of Advent of Code 2025.

This puzzle is about working with **inclusive integer ranges** and determining whether values fall inside them.

---

## Problem Summary

You are given:
- A list of **fresh ingredient ID ranges**
- A list of **available ingredient IDs**

An ingredient ID is **fresh** if it falls inside **any** of the given ranges.


---

## Structure

```text
day5/
│── common.py   # parsing, range merging, helpers
│── part1.py    # count fresh IDs from available list
│── part2.py    # count total fresh IDs from ranges
└── README.md
```

---

## Part 1 — Fresh Ingredient Check

**Goal:**  

Count how many available ingredient IDs are fresh.

### Example

Ranges:

```text
3-5
10-14
16-20
12-18
```

Available IDs:

```text
1
5
8
11
17
32
```

Fresh IDs:

```text
5
11
17
```

**Answer:** `3`

### Approach

1. Parse the ranges and IDs.
2. **Merge overlapping ranges** into clean, non-overlapping intervals.
3. For each ID, check whether it falls inside any merged range.
4. Count how many IDs are fresh.

---

## Part 2 — Total Fresh IDs

**Goal:**  

Ignore the available IDs completely.  
Instead, count **how many unique ingredient IDs** are considered fresh by the ranges alone.

### Example

Merged ranges:

```text
3-5
10-14
16-20
12-18
```

turn into:

```text
3-5
10-20
```

Fresh IDs:

```text
3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
```

**Answer:** `14`

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

## Notes

- `common.py` contains:
  - input parsing
  - merging inclusive ranges into non-overlapping intervals
  - helper functions used by both parts
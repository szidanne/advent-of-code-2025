# Advent of Code 2025 — Day 6  
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![AoC](https://img.shields.io/badge/Advent%20of%20Code-2025-red.svg)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)

Solutions for **Day 6** of Advent of Code 2025.

This puzzle is about reading a **wide math worksheet**, splitting it into independent problems, and evaluating each problem according to its formatting rules.

---

## Problem Summary

You are given a **grid of characters** representing multiple math problems laid out horizontally.

Each problem consists of:
- Several **numbers**
- One **operator** (`+` or `*`) at the bottom
- Problems are separated by a **full column of spaces**

The goal is to:
- Solve each problem individually
- Add all results together to get a **grand total**

---

## Structure

```text
day6/
│── common.py   # grid parsing, helpers, shared logic
│── part1.py    # Part 1: read numbers row-by-row
│── part2.py    # Part 2: read numbers column-by-column (right-to-left)
└── README.md
```

---

## Part 1 — Reading Row by Row

### Rules

- Each number is written **normally**, left-to-right
- Read each **row** to form numbers
- Apply the operator at the bottom
- Sum all problem results

### Example Input

```text
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
```

This represents 4 problems

```text
123 * 45 * 6 = 33210
328 + 64 + 98 = 490
51 * 387 * 215 = 4243455
64 + 23 + 314 = 401
```

The grand total is `33210 + 490 + 4243455 + 401` = `4277556`

---

## Part 2 — Column-wise Reading (Right-to-Left)

### New Rules

- Each column of digits forms a number
- Digits are read top → bottom
- Columns are read right → left
- Operators remain at the bottom

### Same Input, Different Meaning


```text
0        | 1 2 3 | 3 2 8 | 5 1   | 6 4
1        |   4 5 |   6 4 | 3 8 7 | 2 3
2        |     6 |   9 8 | 2 1 5 | 3 1 4
3        |   *   |   +   |   *   |   +
```

This also represents 4 problems

```text
Rightmost problem:
4 + 431 + 623 = 1058

Second from right:
175 * 581 * 32 = 3253600

Third:
8 + 248 + 369 = 625

Leftmost:
356 * 24 * 1 = 8544
```

The grand total is `1058 + 3253600 + 625 + 8544` = `3263827`

---

- Blank columns split independent problems
- Part 1 reads rows
- Part 2 reads columns (right → left)

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
  - grid padding 
  - problem separation 
  - digit extraction 
  - operator application
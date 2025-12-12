# Advent of Code 2025 — Day 3
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![AoC](https://img.shields.io/badge/Advent%20of%20Code-2025-red.svg)](https://adventofcode.com/2025/day/1)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)

Solutions for **Day 3** of Advent of Code 2025.  
This puzzle is about selecting digits from each battery bank to form the **largest possible number**, while **preserving the original order** of the digits.

---

## Problem Summary

Each line of the input represents a **bank of batteries**, written as digits:

```text
987654321111111
```

### Two tasks:

- **Part 1:** Turn on **exactly 2 batteries** per bank 
- **Part 2:** Turn on **exactly 12 batteries** per bank

**The digits you choose:**
- Must stay in their original order
- Are concatenated to form a number
- You want the **largest possible number**

The final answer is the **sum of the best number from each bank**.

---

## Structure

```text
day3/
│── common.py   # shared helpers + core digit-selection logic
│── part1.py    # Part 1: pick the best 2 digits per bank
│── part2.py    # Part 2: pick the best 12 digits per bank
└── README.md
```

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

## How the Solution Works

The key function is `best_k_digits(bank, k)`.

It walks through the digits from **left** to **right** and builds the best possible number using a **stack**.

### Core Idea

- You are allowed to **throw away** some digits
- You throw away **smaller digits** only if a **bigger digit appears** later
- Once you run out of allowed removals, you keep everything

### Visualised Stack

#### Example

```python
bank = "234278"
k = 4
```

We must remove **2 digits** (6 total − 4 kept).

```text
Digits:  2  3  4  2  7  8
--------------------------------
Stack:   []

Read '2'
Stack: [2]

Read '3'
3 > 2 → remove 2
Stack: [3]

Read '4'
4 > 3 → remove 3
Stack: [4]
(no removals left!)

Read '2'
Cannot remove anymore
Stack: [4,2]

Read '7'
Cannot remove anymore
Stack: [4,2,7]

Read '8'
Cannot remove anymore
Stack: [4,2,7,8]
```

**Final result:**

```text
4278
```

## Notes

- `common.py` contains:
  - EXAMPLE input
  - `best_k_digits()` used by both parts 
- Part 1 and Part 2 differ only by the value of k
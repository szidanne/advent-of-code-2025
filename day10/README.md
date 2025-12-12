# Advent of Code 2025 — Day 10  
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![AoC](https://img.shields.io/badge/Advent%20of%20Code-2025-red.svg)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)

Solutions for **Day 10** of Advent of Code 2025.

This puzzle is about recovering the initialization procedure of factory machines using:

- indicator lights (Part 1) — **toggle on/off**
- joltage counters (Part 2) — **increment to exact targets**

---

## Problem Summary

Each machine is described by one line:

```text
[diagram] (button) (button) ... {jolts}
```

-   `[diagram]` is a string of `.` and `#` (goal light states)
-   Each `(button)` lists indices it affects (0-based)
-   `{jolts}` is a list of target counter values

---

## Structure

```text
day10/
│── common.py   # parsing + solvers for both parts
│── part1.py    # Part 1 runner
│── part2.py    # Part 2 runner (Z3 optimizer)
└── README.md
```

---

## Parsing (Both Parts)

Example machine line:

```text
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
```

-   diagram: `.##.` (4 indicator lights)
-   buttons:
    -   (3)
    -   (1,3)
    -   (2)
    -   ...
-   jolts: `3,5,4,7` (4 counters)

We ignore jolts in Part 1 and ignore diagram in Part 2.

---

## Part 1 — Indicator Lights (Toggles)

### Rules

-   The machine has `N` lights, all starting OFF.
-   `.` means the light must be OFF, `#` means ON.
-   Pressing a button toggles the listed lights.
-   You can press buttons any integer number of times.
-   Goal: **minimum total button presses** to match the diagram.

### Key idea: toggles are mod 2

If you press the same button twice, it cancels out (OFF→ON→OFF).

So each light is either:

-   0 (off)
-   1 (on)

### Representation

We represent the whole panel as a bitmask:

-   bit 0 = light 
-   bit 1 = light

Example for `.##.`:

```text
index:  0 1 2 3
state:  . # # .
bits:   0 1 1 0   => binary 0110
```

A button like `(0,2,3)` becomes a mask:

```text
bit 0 on
bit 2 on
bit 3 on
```

Pressing the button is:

```text
state = state XOR button_mask
```

### ASCII toggle idea

```text
Before:  . # . # .
Button:  ^   ^ ^     (toggles 0,3,4)
After:   # # . . .
```

### Approach: BFS overstates

-   start state = all off
-   neighbors = press any button once
-   BFS finds the minimum number of presses

---

## Part 2 — Joltage Counters (Increment)

### Rules

-   Ignore the diagram.
-   Each machine has counters, all starting at 0:

```text
{0,0,0,...}
```

-   Pressing a button increases listed counters by 1.
-   Goal: reach the exact target `{...}` with minimum total presses.

### This is an integer optimization problem

Let:

-   `x_b` = number of times button `b` is pressed (integer, `x_b >= 0`)

Each counter `i` must satisfy:

```text
sum(x_b for buttons that include i) == target[i]
```

Objective:

```text
minimize sum(x_b)
```

### ASCII example

Suppose targets are:

```text
{3,1}
```

Buttons:

```text
A affects (0)
B affects (0,1)
```

Then:

```text
counter 0: A + B = 3
counter 1:     B = 1
=> B = 1
=> A = 2
minimum presses = A + B = 3
```

### Approach: Z3 Optimize

We use Z3 (`z3-solver`) to:

-   create integer variables for button presses
-   add equality constraints for each counter
-   minimize total presses

---

## Run Part 1

#### Reads input from STDIN:

`python3 part1.py < input.txt`

#### Run the built-in example:

`python3 part1.py example`

---

## Run Part 2

#### Install Z3:

`pip install z3-solver`

#### Reads input from STDIN:

`python3 part2.py < input.txt`

#### Run the built-in example:

`python3 part2.py example`

---

## Notes

-   `common.py` contains:
    -   parsing (`parse_machine_line`, `read_machines`)
    -   Part 1 solver (`min_presses_lights`) using BFS over toggle states
    -   Part 2 solver (`min_presses_jolts_z3`) using Z3 optimization
-   Part 1 is fast when the number of lights is small (state space is `2^N`)
-   Part 2 avoids brute force by solving the exact minimum press problem as ILP
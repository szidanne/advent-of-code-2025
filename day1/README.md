# Advent of Code 2025 — Day 1  
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![AoC](https://img.shields.io/badge/Advent%20of%20Code-2025-red.svg)](https://adventofcode.com/2025/day/1)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)

Solutions for **Day 1** of Advent of Code 2025.  
This puzzle simulates rotations on a 100-position safe dial.  
The dial:

- has positions `0–99`
- starts at **50**
- rotates clockwise on `R`, counter-clockwise on `L`
- wraps using modulo arithmetic

The two parts differ in how zero-hits are counted.

---

## Structure

```text
day1/
│── common.py   # shared helpers (parsing, constants, example input)
│── part1.py    # Part 1: count times the dial *ends* at 0
│── part2.py    # Part 2: count times the dial *passes through* 0
└── README.md
```

## Part 1 — Count How Many Times the Dial Ends at Zero

Each instruction is a rotation such as:

```text
L68
R48
L5
```

### Part 1 asks:
> How many times does the dial finish a rotation at position 0?

Only **endpoints** count.

#### Example (from prompt)

Starting at `50`:

```text
L68 → ends on 82
L30 → ends on 52
R48 → ends on 0  (count)
L5  → ends on 95
```

### Run Part 1

#### Reads input from STDIN:


## Part 1 — Count How Many Times the Dial Ends at Zero

Each instruction is a rotation such as:

```text
L68
R48
L5
```

### Part 1 asks:
> How many times does the dial finish a rotation at position 0?

Only **endpoints** count.

#### Example (from prompt)

Starting at `50`:

```text
L68 → ends on 82
L30 → ends on 52
R48 → ends on 0  (count)
L5  → ends on 95
```

### Run Part 1

#### Reads input from STDIN:


## Part 1 — Count How Many Times the Dial Ends at Zero

Each instruction is a rotation such as:

```text
L68
R48
L5
```

### Part 1 asks:
> How many times does the dial finish a rotation at position 0?

Only **endpoints** count.

#### Example (from prompt)

Starting at `50`:

```text
L68 → ends on 82
L30 → ends on 52
R48 → ends on 0  (count)
L5  → ends on 95
```

### Run Part 1

#### Reads input from STDIN:


## Part 1 — Count How Many Times the Dial Ends at Zero

Each instruction is a rotation such as:

```text
L68
R48
L5
```

### Part 1 asks:
> How many times does the dial finish a rotation at position 0?

Only **endpoints** count.

#### Example (from prompt)

Starting at `50`:

```text
L68 → ends on 82
L30 → ends on 52
R48 → ends on 0  (count)
L5  → ends on 95
```

### Run Part 1

#### Reads input from STDIN:


## Part 1 — Count How Many Times the Dial Ends at Zero

Each instruction is a rotation such as:

```text
L68
R48
L5
```

### Part 1 asks:
> How many times does the dial finish a rotation at position 0?

Only **endpoints** count.

#### Example (from prompt)

Starting at `50`:

```text
L68 → ends on 82
L30 → ends on 52
R48 → ends on 0  (count)
L5  → ends on 95
```

### Run Part 1

#### Reads input from STDIN:


## Part 1 — Count How Many Times the Dial Ends at Zero

Each instruction is a rotation such as:

```text
L68
R48
L5
```

### Part 1 asks:
> How many times does the dial finish a rotation at position 0?

Only **endpoints** count.

#### Example (from prompt)

Starting at `50`:

```text
L68 → ends on 82
L30 → ends on 52
R48 → ends on 0  (count)
L5  → ends on 95
```

### Run Part 1

#### Reads input from STDIN:


## Part 1 — Count How Many Times the Dial Ends at Zero

Each instruction is a rotation such as:

```text
L68
R48
L5
```

### Part 1 asks:
> How many times does the dial finish a rotation at position 0?

Only **endpoints** count.

#### Example (from prompt)

Starting at `50`:

```text
L68 → ends on 82
L30 → ends on 52
R48 → ends on 0  (count)
L5  → ends on 95
```

### Run Part 1

#### Reads input from STDIN:


## Part 1 — Count How Many Times the Dial Ends at Zero

Each instruction is a rotation such as:

```text
L68
R48
L5
```

### Part 1 asks:
> How many times does the dial finish a rotation at position 0?

Only **endpoints** count.

#### Example (from prompt)

Starting at `50`:

```text
L68 → ends on 82
L30 → ends on 52
R48 → ends on 0  (count)
L5  → ends on 95
```

### Run Part 1

#### Reads input from STDIN:


## Part 1 — Count How Many Times the Dial Ends at Zero

Each instruction is a rotation such as:

```text
L68
R48
L5
```

### Part 1 asks:
> How many times does the dial finish a rotation at position 0?

Only **endpoints** count.

#### Example (from prompt)

Starting at `50`:

```text
L68 → ends on 82
L30 → ends on 52
R48 → ends on 0  (count)
L5  → ends on 95
```

### Run Part 1

#### Reads input from STDIN:


## Part 1 — Count How Many Times the Dial Ends at Zero

Each instruction is a rotation such as:

```text
L68
R48
L5
```

### Part 1 asks:
> How many times does the dial finish a rotation at position 0?

Only **endpoints** count.

#### Example (from prompt)

Starting at `50`:

```text
L68 → ends on 82
L30 → ends on 52
R48 → ends on 0  (count)
L5  → ends on 95
```

### Run Part 1

#### Reads input from STDIN:

`python3 part1.py < input.txt`

#### Run the built-in example:

`python3 part1.py example`

---

## Part 2 — Count All Times the Dial Passes Through Zero

Method `0x434C49434B` changes the rules:

> Count all times the dial points at 0
> including mid-rotation clicks, not just the final position.

A rotation can pass 0 multiple times, including for large movements such as:

```text
R1000  -> crosses 0 ten times
```

#### Example (from prompt)

Starting at `50`:

```text
L68 crosses 0 once
R48 ends at 0 (count 1)
R60 crosses 0 once
L55 ends at 0 (count 1)
L99 ends at 0 (count 1)
L82 crosses 0 once
```

Total crossings: 6

### Run Part 2

#### Reads input from STDIN:

`python3 part2.py < input.txt`

#### Run the built-in example:

`python3 part2.py example`

## Notes

- `common.py` contains:
 - constants: `START = 50`, `DIAL_SIZE = 100`
 - `parse_move("L68")` → `("L", 68)`
 - example input for testing
# Advent of Code 2025
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![AoC](https://img.shields.io/badge/Advent%20of%20Code-2025-red.svg)](https://adventofcode.com/2025)
![Status](https://img.shields.io/badge/Progress-Ongoing-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Days Completed](https://img.shields.io/badge/Days%20Completed-3%2F12-purple.svg)

This repository contains my solutions to **Advent of Code 2025**, written in Python.  

Each day's solution is isolated in its own folder.

----

# Project Structure

```text
advent-of-code-2025
│── .gitignore
│── aoc_common.py # shared helpers among all days
│── README.md # (this file)
│
└── dayXX/
    │── common.py # day-specific EXAMPLE input + shared helpers
    │── part1.py # Part 1 solution
    │── fetch_input.py # fetches AoC input using environment variables
    │── part2.py # Part 2 solution
    └── README.md # problem-specific explanation
```


# Requirements

- Python **3.10+**
- Standard library usage only (no external dependencies)

# Running Solutions

Reads from STDIN:

```bash
python3 dayXX/part1.py < dayXX/input.txt
python3 dayXX/part2.py < dayXX/input.txt
```

Run built-in example:

```bash
python3 dayXX/part1.py example
python3 dayXX/part2.py example
```


## License

This repository uses the **MIT License**, allowing reuse and modification.
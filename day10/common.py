from collections import deque
from z3 import Int, Optimize, Sum

EXAMPLE = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""


def is_valid_line(s):
    return s is not None and s != ""


def parse_machine_line(line):
    """
    parse a single line into:
      diagram: string like ".##."
      buttons: list of list[int], e.g. [[3], [1,3], [2], ...]
      jolts:   list[int], e.g. [3,5,4,7]
    """
    line = line.strip()

    diagram = None
    buttons = []
    jolts = None

    i = 0
    while i < len(line):
        ch = line[i]

        # diagram: [ ... ]
        if ch == "[":
            i += 1
            start = i
            while i < len(line) and line[i] != "]":
                i += 1
            diagram = line[start:i]
            i += 1
            continue

        # button: ( ... )
        if ch == "(":
            i += 1
            start = i
            while i < len(line) and line[i] != ")":
                i += 1
            inside = line[start:i].strip()
            i += 1

            # inside is like "0,2,3" or "3"
            if inside == "":
                button = []
            else:
                parts = inside.split(",")
                button = []
                for p in parts:
                    p = p.strip()
                    if p != "":
                        button.append(int(p))

            buttons.append(button)
            continue

        # jolts: { ... }
        if ch == "{":
            i += 1
            start = i
            while i < len(line) and line[i] != "}":
                i += 1
            inside = line[start:i].strip()
            i += 1

            parts = inside.split(",")
            jolts_list = []
            for p in parts:
                p = p.strip()
                if p != "":
                    jolts_list.append(int(p))
            jolts = jolts_list
            continue

        i += 1

    if diagram is None:
        raise ValueError("No [diagram] found in line")
    if jolts is None:
        raise ValueError("No {jolts} found in line")

    return diagram, buttons, jolts


def read_machines(lines):
    """
    returns list of machines, each as:
      (diagram, buttons, jolts)
    """
    machines = []
    for line in lines:
        line = line.rstrip("\n")
        if not is_valid_line(line.strip()):
            continue
        machines.append(parse_machine_line(line))
    return machines


# part 1: lights toggle
def diagram_to_goal_mask(diagram):
    """
    convert ".##." into a bitmask goal where:
      '#' => 1
      '.' => 0
    index 0 is the first light.
    """
    mask = 0
    for idx, ch in enumerate(diagram):
        if ch == "#":
            mask |= 1 << idx
    return mask


def button_to_toggle_mask(button_indices):
    """
    convert a button like [0,2,3] into a bitmask with those bits set.
    """
    m = 0
    for idx in button_indices:
        m |= 1 << idx
    return m


def min_presses_lights(diagram, buttons):
    """
    BFS over 2^n states, each state is a bitmask of which lights are ON.
    start state = 0 (all off).
    goal state = mask derived from diagram.
    each button press does: state ^= button_mask
    """
    n = len(diagram)
    goal = diagram_to_goal_mask(diagram)

    button_masks = []
    for b in buttons:
        button_masks.append(button_to_toggle_mask(b))

    start = 0

    q = deque()
    q.append(start)

    dist = {start: 0}

    while q:
        cur = q.popleft()
        if cur == goal:
            return dist[cur]

        cur_steps = dist[cur]

        for bm in button_masks:
            nxt = cur ^ bm
            if nxt not in dist:
                dist[nxt] = cur_steps + 1
                q.append(nxt)

    raise ValueError("No solution found for lights")


def solve_part1(lines):
    machines = read_machines(lines)
    total = 0
    for diagram, buttons, _ in machines:
        total += min_presses_lights(diagram, buttons)
    return total


# part 2: jolts / counters
def min_presses_jolts_z3(target, buttons):
    """
    Z3 optimization for Part 2.

    x_b = number of times button b is pressed (integer, >= 0)

    For each counter i:
        sum(x_b for b that affects i) == target[i]

    Minimize:
        sum(x_b)
    """
    m = len(target)
    k = len(buttons)

    opt = Optimize()

    # Variables: one per button
    x = []
    for b in range(k):
        var = Int(f"x_{b}")
        x.append(var)
        opt.add(var >= 0)

    # Constraints: each counter must match target exactly
    for i in range(m):
        terms = []
        for b in range(k):
            # if button b affects counter i, include x[b] in the sum
            if i in buttons[b]:
                terms.append(x[b])

        if len(terms) == 0:
            # No button ever changes this counter -> only solvable if target is 0
            if target[i] != 0:
                raise ValueError(
                    "No solution: a counter has target != 0 but no buttons affect it"
                )
            continue

        opt.add(Sum(terms) == target[i])

    # Objective: minimize total presses
    opt.minimize(Sum(x))

    result = opt.check()
    if str(result) != "sat":
        raise ValueError("No solution found (unsat/unknown)")

    model = opt.model()

    # Extract solution: sum of x_b
    total = 0
    for b in range(k):
        val = model.evaluate(x[b], model_completion=True).as_long()
        total += val

    return total


def solve_part2(lines):
    machines = read_machines(lines)
    total = 0
    for _, buttons, jolts in machines:
        total += min_presses_jolts_z3(jolts, buttons)
    return total

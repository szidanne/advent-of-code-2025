START = 50
DIAL_SIZE = 100

EXAMPLE = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""


def parse_move(line):
    """
    parses a rotation instruction like:
      L68  -> ("L", 68)
      R5   -> ("R", 5)
    returns None for malformed or empty lines.
    """
    line = line.strip()
    if not line:
        return None

    direction = line[0]
    value_str = line[1:]

    if direction not in ("L", "R"):
        return None
    if not value_str.isdigit():
        return None

    return direction, int(value_str)

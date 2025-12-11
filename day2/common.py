EXAMPLE = """
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
"""


def is_double_repeat_id(n):
    """
    returns True if the decimal representation of n consists of one block
    repeated exactly twice. Example: 1212, 4646, 9999.
    """
    s = str(n)
    l = len(s)
    if l % 2 != 0:
        return False
    mid = l // 2
    return s[:mid] == s[mid:]


def is_repeated_block_id(n):
    """
    returns True if n is composed of a block repeated >=2 times.
    example: 123123123, 1212, 7777777.
    """
    s = str(n)
    l = len(s)

    for d in range(1, l // 2 + 1):
        if l % d != 0:
            continue
        k = l // d
        if k < 2:
            continue

        block = s[:d]
        if s == block * k:
            return True

    return False


def generate_double_repeat_ids(global_min, global_max):
    """
    efficiently generates all numbers in [global_min, global_max] that are
    exactly (block repeated 2 times).
    """
    ids = set()
    max_len = len(str(global_max))

    # only lengths where L = 2d
    for L in range(2, max_len + 1):
        if L % 2 != 0:
            continue

        d = L // 2
        start = 10 ** (d - 1)
        end = 10**d

        for base in range(start, end):
            s = str(base) * 2
            n = int(s)
            if global_min <= n <= global_max:
                ids.add(n)

    return ids


def generate_repeated_block_ids(global_min, global_max):
    """
    generates all numbers in range that are block repeated >=2 times.
    """
    ids = set()
    max_len = len(str(global_max))

    for L in range(2, max_len + 1):
        for d in range(1, L // 2 + 1):
            if L % d != 0:
                continue

            k = L // d
            if k < 2:
                continue

            start = 10 ** (d - 1)
            end = 10**d

            for base in range(start, end):
                s = str(base) * k
                n = int(s)
                if global_min <= n <= global_max:
                    ids.add(n)

    return ids


def parse_ranges(line):
    """
    parses 'A-B,C-D,...' into a list of (A,B) integer pairs.
    """
    ranges = []
    for part in line.strip().split(","):
        if not part:
            continue
        lo, hi = part.split("-")
        ranges.append((int(lo), int(hi)))
    return ranges


def id_in_any_range(n, ranges):
    for lo, hi in ranges:
        if lo <= n <= hi:
            return True
    return False

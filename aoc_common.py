import sys


def read_input(splitlines=True):
    """
    reads from STDIN and returns list of lines.
    """
    raw_data = sys.stdin.read().strip()
    if splitlines:
        return raw_data.splitlines()
    return raw_data


def parse_example(example_block, splitlines=True):
    """
    turns a triple-quoted example string into a line list.
    """
    raw_data = example_block.strip()
    if splitlines:
        raw_data = raw_data.splitlines()
    return raw_data

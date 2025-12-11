import sys


def read_input():
    """
    reads from STDIN and returns list of lines.
    """
    return sys.stdin.read().strip().splitlines()


def parse_example(example_block):
    """
    turns a triple-quoted example string into a line list.
    """
    return example_block.strip().splitlines()

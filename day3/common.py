EXAMPLE = """
987654321111111
811111111111119
234234234234278
818181911112111
"""


def best_k_digits(bank, k):
    bank = bank.strip()
    n = len(bank)

    # if we need all digits, just return the number as-is
    if k >= n:
        return int(bank)

    # if we need zero digits, the result is zero
    if k <= 0:
        return 0

    # how many digits we are allowed to throw away
    to_remove = n - k

    # this list is the number we are building, one digit at a time
    stack = []

    # look at the digits from left to right (start to end)
    for ch in bank:

        # if:
        # - we can still throw digits away
        # - we already picked some digits
        # - the current digit is bigger than the last one we picked
        #
        # then throwing away the smaller digit makes the number bigger
        #
        # example:
        # stack = ['2'], current digit = '7'
        # better number = '7' than '2'
        while to_remove > 0 and stack and stack[-1] < ch:
            stack.pop()  # throw away the smaller digit
            to_remove -= 1

        # keep the current digit
        stack.append(ch)

    # if we still haven't thrown away enough digits,
    # remove them from the end (smallest impact)
    if to_remove > 0:
        stack = stack[:-to_remove]

    # Join the kept digits into the final number
    return int("".join(stack[:k]))

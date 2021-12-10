import numpy as np
from functools import reduce

file = '2021/inputs/d10.txt'


# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]

points_map = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}
autocomplete_points_map = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

def is_open(c):
    return c in ['(', '[', '{', '<']
def is_close(c):
    return c in [')', ']', '}', '>']
close_to_open = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<',
}
open_to_close = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

illegals = []
autocomplete_scores = []
for line in lines:
    # print(line)
    stack = []
    illegal = False
    for c in line:
        if is_open(c):
            stack.append(c)
        elif is_close(c):
            if len(stack) == 0 or close_to_open[c] != stack[-1]:
                illegal = True
                illegals.append(c)
                break
            else:
                stack.pop()
        else:
            raise ValueError

    if not illegal:
        # score = sum(autocomplete_points_map[open_to_close[c]] for c in stack)
        score = reduce(lambda x, y: x * 5 + y, [autocomplete_points_map[open_to_close[c]] for c in stack[::-1]], 0)
        autocomplete_scores.append(score)
        # print(line, [autocomplete_points_map[open_to_close[c]] for c in stack[::-1]], score)

# print(illegals)
print(sum(points_map[c] for c in illegals if c is not None))

# print(autocomplete_scores)
autocomplete_scores = sorted(autocomplete_scores)
# print(len(autocomplete_scores))
print(autocomplete_scores[len(autocomplete_scores)//2])

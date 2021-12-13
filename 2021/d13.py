import numpy as np
from functools import reduce
from collections import defaultdict
from pprint import pprint

file = '2021/inputs/d13.txt'

# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]

dots = np.array([list(map(int, line.split(','))) for line in lines if not line.startswith('fold along ')])
folds = [line[len('fold along '):].split('=') for line in lines if line.startswith('fold along ')]

def dots_to_grid(dots):
    rr_max = dots.max(axis=0)
    rr_min = dots.min(axis=0)
    rr_range = rr_max - rr_min + 1
    grid = np.zeros(rr_range, dtype=int)
    dots = dots - rr_min
    assert (dots >= 0).all()
    grid[dots[:, 0], dots[:, 1]] = 1
    return grid

for i, (axis, val) in enumerate(folds):
    val = int(val)
    if axis == 'x':
        xy0 = dots[dots[:, 0] < val].copy()
        xy1 = dots[dots[:, 0] >= val].copy()
        xy1[:,0] = 2*val - xy1[:,0]
        dots = np.unique(np.concatenate((xy0, xy1), axis=0), axis=0)
    elif axis == 'y':
        xy0 = dots[dots[:, 1] < val].copy()
        xy1 = dots[dots[:, 1] >= val].copy()
        xy1[:,1] = 2*val - xy1[:,1]
        dots = np.unique(np.concatenate((xy0, xy1), axis=0), axis=0)
    if i == 0:
        print('P1', dots.shape[0])

print('P2')
f = dots_to_grid(dots).T
print('\n'.join([''.join(['#' if x else ' ' for x in f]) for f in f]))

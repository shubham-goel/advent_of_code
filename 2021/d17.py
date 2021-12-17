from typing import Dict, List
import numpy as np
from pprint import pprint
from numba import jit, njit

file = '2021/inputs/d17.txt'

# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]

Rx, Ry = lines[0].replace('target area: ', '').split(', ')
Rx = list(map(int, Rx[len('x='):].split('..')))
Ry = list(map(int, Ry[len('y='):].split('..')))
print(Rx, Ry)


def position_x(vx, t):
    if t > vx:
        # px = vx + (vx-1) + (vx-2) + ... + 1
        px = (vx*(vx + 1)) // 2
    else:
        # px = vx + (vx-1) + (vx-2) + ... + (vx-t+1)
        px = (t * (vx + vx - t + 1)) // 2
    return px

def position_y(vy, t):
    # py = vy + (vy-1) + (vy-2) + ... + (vy-t+1)
    py = (t * (vy + vy - t + 1)) // 2
    return py


def in_region(p_, R_):
    return (R_[0] <= p_ <= R_[1])


def find_best_traj(Rx, Ry):
    vy_max = abs(Ry[0])
    vy_min = -abs(Ry[0])
    for vy in np.arange(vy_min, vy_max+1)[::-1]:
        # Find valid t
        for t in range(1_000_000):
            py = position_y(vy, t)
            if (py < Ry[0]) and ((vy - t) <= 0):
                # Already exceeded bounds
                break
            if in_region(py, Ry):
                # print('valid', vy, t, py)
                for vx in range(1, 1_000_000):
                    px = position_x(vx, t)
                    if px > Rx[1]:
                        break
                    if in_region(px, Rx):
                        return vx, vy
                # Didn't find valid vx. Continue searching
    return None

def find_all_trajs(Rx, Ry):
    vy_max = abs(Ry[0])
    vy_min = -abs(Ry[0])
    possibilities = []
    for vy in np.arange(vy_min, vy_max+1)[::-1]:
        # Find valid t
        for t in range(1_000_000):
            py = position_y(vy, t)
            if (py < Ry[0]) and ((vy - t) <= 0):
                # Already exceeded bounds
                break
            if in_region(py, Ry):
                # print('valid', vy, t, py)
                for vx in range(1, 1_000_000):
                    px = position_x(vx, t)
                    if px > Rx[1]:
                        break
                    if in_region(px, Rx):
                        possibilities.append((vx, vy))
                # Didn't find valid vx. Continue searching
    return possibilities

vx, vy = find_best_traj(Rx, Ry)
print(vx, vy)
print('P1', position_y(vy, vy))

possibilities = find_all_trajs(Rx, Ry)
possibilities = np.unique(np.array(possibilities), axis=0)
print('P2', len(possibilities))

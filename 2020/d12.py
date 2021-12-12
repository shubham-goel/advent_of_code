from typing import List, Set, Tuple
import numpy as np
from functools import lru_cache
from numba import jit

file = '2020/inputs/d12.txt'


# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]

def update_pos(pos, dir, command):
    c = command[0]
    v = int(command[1:])
    if c in ['N', 'S', 'E', 'W']:
        if c == 'N':
            pos[1] += v
        elif c == 'S':
            pos[1] -= v
        elif c == 'E':
            pos[0] += v
        elif c == 'W':
            pos[0] -= v
    elif c == 'F':
        dir = dir%360
        if dir == 0:
            pos[0] += v
        elif dir == 90:
            pos[1] += v
        elif dir == 180:
            pos[0] -= v
        elif dir == 270:
            pos[1] -= v
        else:
            raise Exception('Invalid direction')
    elif c == 'R':
        dir -= v
    elif c == 'L':
        dir += v
    else:
        raise Exception('Invalid command')
    return pos, dir

DIR = 0 # EAST
POS = [0,0]

for cv in lines:
    POS, DIR = update_pos(POS, DIR, cv)

print(POS, DIR)
print('P1', abs(POS[0]) + abs(POS[1]))


## Part 2
def rotate(pos, angle):
    x, y = pos[0], pos[1]
    angle = angle%360
    if angle == 0:
        return [x, y]
    elif angle == 90:
        return [y, -x]
    elif angle == 180:
        return [-x, -y]
    elif angle == 270:
        return [-y, x]
    else:
        raise Exception('Invalid angle')

def update_pos_way(pos, way, command):
    c = command[0]
    v = int(command[1:])
    if c in ['N', 'S', 'E', 'W']:
        if c == 'N':
            way[1] += v
        elif c == 'S':
            way[1] -= v
        elif c == 'E':
            way[0] += v
        elif c == 'W':
            way[0] -= v
    elif c == 'F':
        pos[0] += way[0]*v
        pos[1] += way[1]*v
    elif c == 'R':
        way = rotate(way, v)
    elif c == 'L':
        way = rotate(way, -v)
    else:
        raise Exception('Invalid command')
    return pos, way


WAY = [10,1] # EAST
POS = [0,0]

for cv in lines:
    POS, WAY = update_pos_way(POS, WAY, cv)

print(POS, WAY)
print('P2', abs(POS[0]) + abs(POS[1]))

import ast
import copy
from functools import lru_cache, reduce
from typing import final
import numpy as np
from numba import jit, njit, prange
from tqdm import tqdm

file = '2021/inputs/d21.txt'

# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]

pos1 = int(lines[0].split(' ')[-1]) - 1
pos2 = int(lines[1].split(' ')[-1]) - 1

DIE_ROLLED = 0
def die():
    global DIE_ROLLED
    DIE_ROLLED = 1 + DIE_ROLLED
    return (DIE_ROLLED - 1)%100 + 1

def move(pos, score):
    pos = (pos + die() + die() + die())%10
    score += pos+1
    return pos, score

score1 = 0
score2 = 0
while True:
    pos1, score1 = move(pos1, score1)
    if score1 >= 1000:
        # p1 wins
        print('Part 1:', score2*DIE_ROLLED)
        break
    pos2, score2 = move(pos2, score2)
    if score2 >= 1000:
        # p2 wins
        print('Part 1:', score1*DIE_ROLLED)
        break


# Part 2
@lru_cache(maxsize=None)
def num_wins_quantum(pos1, pos2, score1, score2):
    p1_wins = 0
    p2_wins = 0
    for d1 in range(1,4):
        for d2 in range(1,4):
            for d3 in range(1,4):
                pos1_next = (d1+d2+d3+pos1)%10
                score1_next = score1 + (pos1_next+1)
                if score1_next >= 21:
                    p1_wins += 1
                else:
                    w2,w1 = num_wins_quantum(pos2, pos1_next, score2, score1_next)
                    p1_wins += w1
                    p2_wins += w2
    return p1_wins, p2_wins


pos1 = int(lines[0].split(' ')[-1]) - 1
pos2 = int(lines[1].split(' ')[-1]) - 1
w1,w2 = num_wins_quantum(pos1, pos2, 0, 0)
print(w1,w2)
print('Part 2:', max(w1,w2))

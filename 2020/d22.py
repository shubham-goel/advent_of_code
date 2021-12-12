from typing import List, Set, Tuple
import numpy as np
from functools import lru_cache
from numba import jit

file = '2020/inputs/d22.txt'


# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]

assert(lines[0] == 'Player 1:')
i = lines.index('Player 2:')
D1 = list(map(int, lines[1:i]))
D2 = list(map(int, lines[i+1:]))

# @jit
def move(d1: list, d2: list):
    a = d1.pop(0)
    b = d2.pop(0)
    if a > b:
        d1.append(a)
        d1.append(b)
    else:
        d2.append(b)
        d2.append(a)
    if len(d1) == 0:
        return 2
    elif len(d2) == 0:
        return 1
    else:
        return 0

D1_og = D1.copy()
D2_og = D2.copy()
while True:
    m = move(D1, D2)
    m = 1
    if m == 1:
        winner = D1
        break
    elif m == 2:
        winner = D2
        break

winner = np.array(winner)
print(f'Winner {m}: {winner}')
print('P1', (winner[::-1] * (np.arange(winner.size)+1)).sum())


# Part 2
def get_config(d1: list, d2: list):
    return tuple(d1), tuple(d2)

GAME_COUNTER = 0
def game(d1: Tuple[int], d2: Tuple[int]) -> Tuple[int, list]:
    global GAME_COUNTER
    GAME_COUNTER = GAME_COUNTER + 1
    gnum = GAME_COUNTER
    # print(f'\n\nNew game {gnum}!', len(d1), len(d2))
    previous_configs = set()

    rnum = 0
    while True:
        # print(f"G{gnum} Player 1's deck:", d1)
        # print(f"G{gnum} Player 2's deck:", d2)
        m = round(d1, d2, previous_configs, gnum=gnum, rnum=rnum)
        if m == 1:
            return 1, d1
        elif m == 2:
            return 2, d2
        rnum+=1

def round(d1: list, d2: list, previous_configs: set, gnum=-1, rnum=-1) -> int:
    config = get_config(d1, d2)
    if config in previous_configs:
        # print('Loop detected!')
        return 1    # player 1 won game
    previous_configs.add(config)

    a = d1.pop(0)
    b = d2.pop(0)

    if len(d1) >= a and len(d2) >= b:
        # print(f'G{gnum} Playing a subgame!')
        round_winner, _ = game(d1[:a], d2[:b])
        # print(f'Back to parent game G{gnum}')
    else:
        round_winner = 1 if a>b else 2

    if round_winner==1:
        # print(f' G{gnum} 1 won round R{rnum}!')
        d1.append(a)
        d1.append(b)
    else:
        # print(f' G{gnum} 2 won round R{rnum}!')
        d2.append(b)
        d2.append(a)

    if len(d1) == 0:
        return 2    # player 2 won game
    elif len(d2) == 0:
        return 1    # player 1 won game
    else:
        return 0

m, winner = game(D1_og.copy(), D2_og.copy())
winner = np.array(winner)
print(f'Winner {m}: {winner}')
print('P2', (winner[::-1] * (np.arange(winner.size)+1)).sum())

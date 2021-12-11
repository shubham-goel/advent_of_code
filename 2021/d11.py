import numpy as np
from functools import reduce

file = '2021/inputs/d11.txt'


# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]

E = np.array(
    [list(map(int, line)) for line in lines],
)
print(E)

def move(E):
    E = E+1
    flashed = np.zeros_like(E, dtype=bool)
    while True:
        just_flashed = (E>9) & ~flashed
        flashed |= just_flashed
        if just_flashed.sum() == 0:
            break
        E[1:, 1:] += just_flashed[:-1, :-1] # Bottom right
        E[:-1, 1:] += just_flashed[1:, :-1] # Bottom left
        E[1:, :-1] += just_flashed[:-1, 1:] # Top right
        E[:-1, :-1] += just_flashed[1:, 1:] # Top left
        E[:, 1:] += just_flashed[:, :-1] # Bottom
        E[:, :-1] += just_flashed[:, 1:] # Top
        E[:-1, :] += just_flashed[1:, :] # Left
        E[1:, :] += just_flashed[:-1, :] # Right
    E[flashed] = 0
    return E, flashed.sum()

## Part 1
STEPS = 100
num_flashed = []
E_og = E.copy()
for i in range(STEPS):
    E, n = move(E)
    num_flashed.append(n)
print(num_flashed)
print('P1', sum(num_flashed))

## Part 2
E = E_og.copy()
for i in range(int(1e10)):
    E, n = move(E)
    if n == E.size:
        print('P2', i+1)
        break

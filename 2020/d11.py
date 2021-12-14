import numpy as np
from pprint import pprint
from numba import jit

file = '2020/inputs/d11.txt'

# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]

S = np.array([[1 if x=='L' else 0 for x in line] for line in lines])

def count_adj_occupied(S):
    occ = S==2
    counts = np.zeros_like(S)
    # Add counts to 8 adjacent squares
    counts[1:,:] += occ[:-1,:]
    counts[:-1,:] += occ[1:,:]
    counts[:,1:] += occ[:,:-1]
    counts[:,:-1] += occ[:,1:]
    counts[1:,1:] += occ[:-1,:-1]
    counts[1:,:-1] += occ[:-1,1:]
    counts[:-1,1:] += occ[1:,:-1]
    counts[:-1,:-1] += occ[1:,1:]
    return counts

def move(S):
    # print(S)
    counts = count_adj_occupied(S)
    # print(counts)
    occ1 = (S==1) & (counts==0)
    occ0 = (S==2) & (counts>=4)
    S[occ1] = 2
    S[occ0] = 1
    return occ1.sum() + occ0.sum()

S_og = S.copy()
while True:
    changed = move(S)
    # print(changed, (S==2).sum())
    if changed == 0:
        break

print('P1', (S==2).sum())

# @jit(nopython=True, parallel=True)
def count_adj_occupied_part2(S):
    occ = S==2
    counts = np.zeros_like(S)
    # Add counts to 8 adjacent squares
    for i in range(S.shape[0]):
        for j in range(S.shape[1]):
            if S[i,j] >= 1:
                for a in range(i+1, S.shape[0]):
                    if (x := S[a,j]) >= 1:
                        if x == 2: counts[i,j] += 1
                        break
                for a in reversed(range(0, i)):
                    if (x := S[a,j]) >= 1:
                        if x == 2: counts[i,j] += 1
                        break
                for b in range(j+1, S.shape[1]):
                    if (x := S[i,b]) >= 1:
                        if x == 2: counts[i,j] += 1
                        break
                for b in reversed(range(0, j)):
                    if (x := S[i,b]) >= 1:
                        if x == 2: counts[i,j] += 1
                        break
                for a,b in zip(range(i+1, S.shape[0]), range(j+1, S.shape[1])):
                    if (x := S[a,b]) >= 1:
                        if x == 2: counts[i,j] += 1
                        break
                for a,b in zip(reversed(range(0,i)), range(j+1, S.shape[1])):
                    if (x := S[a,b]) >= 1:
                        if x == 2: counts[i,j] += 1
                        break
                for a,b in zip(range(i+1, S.shape[0]), reversed(range(0, j))):
                    if (x := S[a,b]) >= 1:
                        if x == 2: counts[i,j] += 1
                        break
                for a,b in zip(reversed(range(0,i)), reversed(range(0, j))):
                    if (x := S[a,b]) >= 1:
                        if x == 2: counts[i,j] += 1
                        break
    return counts

def move2(S):
    # print(S)
    counts = count_adj_occupied_part2(S)
    # print(counts)
    occ1 = (S==1) & (counts==0)
    occ0 = (S==2) & (counts>=5)
    S[occ1] = 2
    S[occ0] = 1
    return occ1.sum() + occ0.sum()

S = S_og.copy()
while True:
    changed = move2(S)
    # print(changed, (S==2).sum())
    if changed == 0:
        break

print('P2', (S==2).sum())

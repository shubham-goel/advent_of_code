import ast
import copy
from functools import reduce
from typing import final
import numpy as np
from numba import jit, njit, prange
from tqdm import tqdm

file = '2021/inputs/d20.txt'

# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]

algo = lines[0]
inp = np.array([[0 if x=='.' else 1 for x in l] for l in lines[1:]])
H = len(inp)
W = len(inp[0])
inp_padded = np.pad(inp, 100, 'constant', constant_values=0)

def refine_img(inp_padded, algo):
    H = len(inp_padded)-2
    W = len(inp_padded[0])-2
    new_inp = np.zeros_like(inp_padded)
    for i in prange(H):
        for j in prange(W):
            region = inp_padded[i:i+3, j:j+3]
            s = list(region[0]) + list(region[1]) + list(region[2])
            s = ''.join(['0' if x==0 else '1' for x in s])
            s = int(s, 2)
            n = algo[s]
            # print((i, j),inp_padded[i+1, j+1], s, n)
            new_inp[i+1, j+1] = 0 if n=='.' else 1
    return new_inp

print(len(algo), algo)
# print(inp_padded)
final_p1 = refine_img(inp_padded, algo)[1:-1, 1:-1]
# print(final_p1)
final_p1 = refine_img(final_p1, algo)[1:-1, 1:-1]
print(final_p1)
print('P1', final_p1.sum())

curr = inp_padded
for _ in tqdm(range(50)):
    curr = refine_img(curr, algo)[1:-1, 1:-1]
print('P2', curr.sum())

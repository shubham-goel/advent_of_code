from typing import Dict, List
import numpy as np
from pprint import pprint
from numba import jit

file = '2021/inputs/d15.txt'

# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]

A = np.array([[int(x) for x in line] for line in lines])

@jit(nopython=True)
def create_R(A):
    R = np.zeros_like(A)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            # Come from top
            t = A[i,j] + R[i-1,j] if i > 0 else A[i,j]
            # Come from left
            l = A[i,j] + R[i,j-1] if j > 0 else A[i,j]

            if i>0 and j>0:
                # Minimum risk
                R[i,j] = min(t, l)
            elif i>0:
                R[i,j] = t
            elif j>0:
                R[i,j] = l
            else:
                R[i,j] = A[i,j]
    return R

@jit(nopython=True)
def refine(A, R):
    while True:
        a = (A[1:,:] + R[:-1,:] < R[1:,:])
        if a.any(): # Come from left
            R[1:,:] = np.minimum(A[1:,:] + R[:-1,:] , R[1:,:])
        b = (A[:, 1:] + R[:, :-1] < R[:,1:])
        if b.any(): # Come from top
            R[:,1:] = np.minimum(A[:, 1:] + R[:, :-1] , R[:,1:])
        c = (A[:-1,:] + R[1:,:] < R[:-1,:])
        if c.any(): # Come from right
            R[:-1,:] = np.minimum(A[:-1,:] + R[1:,:] , R[:-1,:])
        d = (A[:,:-1] + R[:,1:] < R[:,:-1])
        if d.any(): # Come from bottom
            R[:,:-1] = np.minimum(A[:,:-1] + R[:,1:] , R[:,:-1])
        if not (a.any() or b.any() or c.any() or d.any()):
            break
    return R

R = create_R(A)
R = refine(A, R)
print('P1', R[-1,-1] - A[0,0])

A = np.concatenate([np.concatenate([(A+i+j-1)%9+1 for i in range(5)], axis=0) for j in range(5)], axis=1)
R = create_R(A)
R = refine(A, R)
print('P2', R[-1,-1] - A[0,0])

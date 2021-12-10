import numpy as np

file = '2021/inputs/d7.txt'


# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]

x = np.array([int(x) for x in lines[0].split(',')])
med = np.median(x)
print(med, np.abs(x - med).sum())

f = lambda _x: (_x*(_x+1))/2
sol = x.mean() - 0.5

print(sol)
print(f(np.abs(x-sol).sum()))
print(f(np.abs(x-int(sol))).sum())
print(f(np.abs(x-int(sol+1))).sum())

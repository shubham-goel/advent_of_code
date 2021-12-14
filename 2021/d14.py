from typing import Dict, List
import numpy as np
from pprint import pprint
from numba import jit

file = '2021/inputs/d14.txt'

# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]

start = lines[0]
rules: Dict[str, str] = {x:y for x,y in [line.split(' -> ') for line in lines[1:]]}

polymer = list(start)

def step(poly: List[str]) -> List[str]:
    new_poly = [poly[0]]
    for i in range(len(poly)-1):
        a,b = poly[i], poly[i+1]
        try:
            c = rules[a+b]
            new_poly.extend([c,b])
        except KeyError:
            new_poly.extend([b])
    return new_poly

for i in range(10):
    polymer = step(polymer)

def num_max(l):
    # Find how many times the most common element occurs in list
    return max(l.count(x) for x in set(l))
def num_min(l):
    # Find how many times the least common element occurs in list
    return min(l.count(x) for x in set(l))

print('P1', num_max(polymer) - num_min(polymer))


elements = sorted(list(set.union(*[set(x) for x in rules.keys()])))
N = len(elements)
elems_id = {e:elements.index(e) for e in elements}
rules_fast = np.zeros((N, N), dtype=int)
for a,b in rules.items():
    rules_fast[elems_id[a[0]], elems_id[a[1]]] = elems_id[b]

def step_fast(poly):
    first = poly[:-1]
    second = poly[1:]
    added = rules_fast[first, second]
    c = np.empty((poly.size + added.size,), dtype=poly.dtype)
    c[0::2] = poly
    c[1::2] = added
    return c

## Count number of elements in all polymers if initialized with size2
counts  = np.zeros((N,N,N), dtype=int)
for i in range(N):
    for j in range(N):
        curr = np.array([i,j], dtype=int)
        for _ in range(20):
            curr = step_fast(curr)
        counts[i,j] = np.bincount(curr[1:-1])

# Build polymer for 20 steps
polymer = np.array([elems_id[x] for x in start])
for i in range(20):
    print(i, len(polymer))
    # print(''.join(polymer))
    polymer = step_fast(polymer)

# Find counts of elemnts between adjacent elements, if polymer was built for another 20 steps
final_counts = np.bincount(polymer)
for i in range(len(polymer)-1):
    final_counts += counts[polymer[i], polymer[i+1]]

pprint(elems_id)
pprint(final_counts)

print('P2', final_counts.max() - final_counts.min())

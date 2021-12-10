import numpy as np

file = '2021/inputs/d1.txt'


# Read the file
with open(file) as f:
    depths = np.array([int(line.strip()) for line in f if line.strip()])

## Part1
def num_increased(xxx):
    return (xxx[1:] > xxx[:-1]).sum()
print(f'd1: {num_increased(depths)}')

## Part2
smooth_depths = depths[:-2] + depths[1:-1] + depths[2:]
print(f'd2: {num_increased(smooth_depths)}')


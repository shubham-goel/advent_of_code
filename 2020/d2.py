import numpy as np

file = '2020/inputs/d2.txt'


# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]


## Part1
print('## Part1 ##')
splits = [line.split(': ') for line in lines]
policy = [s[0] for s in splits]
passws = [s[1] for s in splits]

occur_item = [p.split()[1] for p in policy]
occur_minmax = [p.split()[0] for p in policy]
occur_min = np.array([int(p.split('-')[0]) for p in occur_minmax])
occur_max = np.array([int(p.split('-')[1]) for p in occur_minmax])

counts = np.array([passws[i].count(occur_item[i]) for i in range(len(policy))])
is_valid = (occur_min <= counts) & (counts <= occur_max)
print(is_valid.sum())

## Part2
print('## Part2 ##')
pos1_contains = np.array([passws[i][occur_min[i]-1] == occur_item[i] for i in range(len(policy))])
pos2_contains = np.array([passws[i][occur_max[i]-1] == occur_item[i] for i in range(len(policy))])
is_valid = np.logical_xor(pos1_contains, pos2_contains)
print(is_valid.sum())

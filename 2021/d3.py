import numpy as np

file = '2021/inputs/d3.txt'


# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]

## Part 1
arrays = np.array([[int(x) for x in line] for line in lines])
arrays = arrays * 2 - 1 # 0->-1, 1->+1
binarr_to_int = lambda x: np.sum(np.abs(x))
gamma = int(''.join([('1' if x>0 else '0') for x in arrays.sum(axis=0) > 0]), 2)
other = int(''.join([('0' if x>0 else '1') for x in arrays.sum(axis=0) > 0]), 2)
print(gamma, other, gamma*other)

## Part 2
arrays = (arrays+1)/2
arrays_filtered = arrays.copy()
for idx in range(arrays.shape[1]):
    if arrays_filtered.shape[0] == 1:
        break
    most_common = (1 if (arrays_filtered*2-1).sum(axis=0)[idx] >= 0 else 0)
    print(most_common, (arrays_filtered*2-1).sum(axis=0))
    mask = (arrays_filtered[:, idx] == most_common)
    arrays_filtered = arrays_filtered[mask, :]
    print(arrays_filtered)
X1 = int(''.join([('1' if x>0 else '0') for x in arrays_filtered[0] > 0]), 2)
print('#####')
arrays_filtered = arrays.copy()
for idx in range(arrays.shape[1]):
    if arrays_filtered.shape[0] == 1:
        break
    least_common = (0 if (arrays_filtered*2-1).sum(axis=0)[idx] >= 0 else 1)
    print(least_common, (arrays_filtered*2-1).sum(axis=0))
    mask = (arrays_filtered[:, idx] == least_common)
    if mask.sum() == 0:
        mask = ~mask
    arrays_filtered = arrays_filtered[mask, :]
    print(arrays_filtered)
X2 = int(''.join([('1' if x>0 else '0') for x in arrays_filtered[0] > 0]), 2)

print(X1, X2, X1*X2)

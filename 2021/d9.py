import numpy as np

file = '2021/inputs/d9.txt'


# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]

A = np.array([[int(x) for x in line] for line in lines])
A = np.pad(A, 1, mode='constant', constant_values=A.max() + 1)

low_points = (A[1:-1,1:-1] < np.minimum(np.minimum(A[:-2,1:-1], A[2:,1:-1]), np.minimum(A[1:-1,2:], A[1:-1,:-2])))
low_points_idx = np.where(low_points)
risk = (A[1:-1,1:-1][low_points_idx]+1).sum()
print(risk)


# Part 2
from scipy.ndimage.morphology import binary_dilation
mask = A[1:-1,1:-1] < 9
cluster_sizes = []
for i in range(len(low_points_idx[0])):
    start = np.zeros_like(A[1:-1,1:-1], dtype=bool)
    start[low_points_idx[0][i], low_points_idx[1][i]] = True

    cluster = binary_dilation(start, mask=mask, iterations=-1)
    cluster_sizes.append(cluster.sum())

print(cluster_sizes)
print(np.prod(sorted(cluster_sizes)[-3:]))

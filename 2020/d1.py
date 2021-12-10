import numpy as np

file = '2020/inputs/d1.txt'


# Read the file
with open(file) as f:
    lines = [line for line in f if line.strip()]

## Part1
print('## Part1 ##')
X = np.array([int(i) for i in lines])
X_sorted = np.sort(X)

for i,x in enumerate(X_sorted):
    j = np.searchsorted(X_sorted, 2020 - x)
    if i!=j and j<X_sorted.size and (X_sorted[j] == 2020 - x):
        y = X_sorted[j]
        print(x, y, x*y)
        print('Part1:', x*y)
        break

## Part2
print('## Part2 ##')
for i,x in enumerate(X_sorted):
    for j in range(i+1, X_sorted.size):
        y = X_sorted[j]
        if x + 2*y <= 2020:
            k = np.searchsorted(X_sorted, 2020 - x - y)
            if j<k<X_sorted.size and (X_sorted[k] == 2020 - x - y):
                z = X_sorted[k]
                print(x, y, z, x+y+z, x*y*z)
                print('Part2:', x*y*z)
                break

import numpy as np

file = '2020/inputs/d3.txt'


# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]


## Part1
print('## Part1 ##')
h = len(lines)
w = len(lines[0])

dW = 3
dH = 1

def sol(dh, dw):
    counter = 0
    for k, i in enumerate(range(0, h, dh)):
        j = k*dw % w
        if lines[i][j] == '#':
            counter = counter + 1
    return counter

print(sol(dH, dW))

print('## Part2 ##')
slopes = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]
sols = np.array([sol(dh, dw) for dw, dh in slopes])
for (dW,dH),s in zip(slopes, sols):
    print(dW,dH, s)
print(np.prod(sols))

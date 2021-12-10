import numpy as np

file = '2021/inputs/d5.txt'


# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]

segments = np.array([[[int(x) for x in pt.strip().split(',')] for pt in line.split('->')] for line in lines])
print(segments.shape)

## Part 1
maxX = segments[:,:,0].max()
maxY = segments[:,:,1].max()
lattice = np.zeros((maxX+1, maxY+1), dtype=int)

for (start, end) in segments:
    if (start[0] == end[0]):
        s,e = min(start[1], end[1]), max(start[1], end[1])
        lattice[start[0], s:e+1] += 1
    if (start[1] == end[1]):
        s,e = min(start[0], end[0]), max(start[0], end[0])
        lattice[s:e+1, start[1]] += 1
    
    # Consider diagnoal lines also
    if abs(start[0] - end[0]) == abs(start[1] - end[1]):
        Xs = np.linspace(start[0], end[0], num=abs(start[0] - end[0])+1).astype(int)
        Ys = np.linspace(start[1], end[1], num=abs(start[1] - end[1])+1).astype(int)
        lattice[Xs, Ys] += 1

    # print(start, end)
    # print(lattice)

print(lattice.T)
print((lattice > 1).sum())

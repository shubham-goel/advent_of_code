import numpy as np
from tqdm import tqdm

## Part 1
circle = [int(x) for x in '614752839']
# circle = [int(x) for x in '389125467']
circle = circle + list(range(10,1000000))
circle = np.array(circle) - 1
current = circle[0]

circle_inv = np.empty_like(circle)
circle_inv[circle] = np.arange(circle.size)

N = len(circle)
# MOVES = 10
MOVES = 10000000
def move(circle, circle_inv, current):
    curr_index = circle_inv[current]
    picked_index = [(curr_index+i+1)%N for i in range(3)]
    picked = [circle[i] for i in picked_index]
    # picked_mask = np.zeros(N, dtype=bool)
    # picked_mask[picked_index] = True
    if picked_index[2] > 2:
        remaining = np.concatenate((circle[:picked_index[0]], circle[picked_index[2]+1:]), axis=0)
    else:
        remaining = circle[picked_index[2]+1 : picked_index[0]].copy()
    assert(remaining.size == N-3)
    destination = current - 1
    if destination <0:
        destination = N-1
    while destination in picked:
        destination -= 1
        if destination <0:
            destination = N-1
    dest_index = circle_inv[destination]
    if dest_index > picked_index[2]:
        dest_index -= min(3, picked_index[2]+1)
    # dest_index = remaining.index(destination)
    # new_circle = np.empty_like(circle)
    circle[:dest_index+1] = remaining[:dest_index+1] 
    circle[dest_index+1:dest_index+1+3] = np.array(picked)
    circle[dest_index+1+3:] = remaining[dest_index+1:]
    # circle = circle
    # circle_inv = np.empty_like(circle)
    circle_inv[circle] = np.arange(circle.size)
    curr_index = circle_inv[current]
    next_current = circle[(curr_index+1)%N]
    return circle, circle_inv, next_current

for _ in tqdm(range(MOVES)):
# for _ in (range(MOVES)):
    circle, circle_inv, current = move(circle, circle_inv, current)
    # print(current+1, ''.join(map(str, circle+1)))

idx_1 = circle_inv[0]
print([circle[(idx_1+i)%N] for i in range(5)])
# 189372645

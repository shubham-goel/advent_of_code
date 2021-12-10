import numpy as np

file = '2021/inputs/d6.txt'


# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]

x = np.array([int(x) for x in lines[0].split(',')])

days = 256
# for i in range(days):
#     x = x-1
#     new_fish = (x<0).sum()
#     x[x<0] = 6
#     x = np.concatenate([x, np.full(new_fish, 8)])
#     # print(x)

#     print(i, x.shape)


num_fish = np.zeros(9, dtype=int)
for _x in x:
    num_fish[_x] += 1
for i in range(days):
    new_fish = num_fish[0]
    num_fish = np.roll(num_fish, -1)
    num_fish[6] += new_fish

    print(num_fish, num_fish.sum())
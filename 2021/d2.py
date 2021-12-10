import numpy as np

file = '2021/inputs/d2.txt'


# Read the file
with open(file) as f:
    lines = [line for line in f if line.strip()]

## Part1
print('## Part1 ##')
splits = [line.split() for line in lines]
actions = [split[0] for split in splits]

def actions_to_code(a):
    if a == 'forward': return 1
    elif a == 'up': return 2
    elif a == 'down': return 3
    else: raise ValueError('Invalid action')
actions_code = np.array([actions_to_code(a) for a in actions])
distances = np.array([int(split[1]) for split in splits])

Xs = np.cumsum(distances * (actions_code==1))
Ys = np.cumsum(distances * ((actions_code==3)*1 + (actions_code==2)*-1))

print(Xs[-1] , Ys[-1])
print(Xs[-1] * Ys[-1])

## Part2
print('## Part2 ##')
aims = np.concatenate((Ys[:1]*0, Ys), axis=0)
Ys = np.cumsum(aims[:-1] * (distances * (actions_code==1)))

print(Xs[-1] , Ys[-1])
print(Xs[-1] * Ys[-1])

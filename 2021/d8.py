import numpy as np

file = '2021/inputs/d8.txt'


# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]

lines1 = [line.split(' | ') for line in lines]
inputs = [line[0].split(' ') for line in lines1]
outputs = [line[1].split(' ') for line in lines1]
for i,o in zip(inputs, outputs):
    print(' '.join(i), '|', ' '.join(o))

outputs_sizes = np.array([[len(x) for x in line] for line in outputs])
print(outputs_sizes)

num_1 = np.sum(outputs_sizes == 2)
num_4 = np.sum(outputs_sizes == 4)
num_7 = np.sum(outputs_sizes == 3)
num_8 = np.sum(outputs_sizes == 7)
print(num_1, num_4, num_7, num_8)
print(num_1 + num_4 + num_7 + num_8)

## Part 2
output_numbers = []
for inp, out in zip(inputs, outputs):
    input_sets = [frozenset(i) for i in inp]
    input_sizes = np.array([len(i) for i in input_sets])
    sets = [None] * 10
    sets[1] = input_sets[np.where(input_sizes == 2)[0][0]]
    sets[4] = input_sets[np.where(input_sizes == 4)[0][0]]
    sets[7] = input_sets[np.where(input_sizes == 3)[0][0]]
    sets[8] = input_sets[np.where(input_sizes == 7)[0][0]]
    set_235_idx = np.where(input_sizes == 5)[0]
    set_069_idx = np.where(input_sizes == 6)[0]
    for i in set_235_idx:
        if sets[1].issubset(input_sets[i]):
            sets[3] = input_sets[i]
        elif (sets[4]-sets[1]).issubset(input_sets[i]):
            sets[5] = input_sets[i]
        else:
            sets[2] = input_sets[i]
    
    sets[9] = sets[8] - (sets[2]-sets[3])
    for i in set_069_idx:
        if len(sets[1].union(input_sets[i]))==7:
            sets[6] = input_sets[i]
        elif len(sets[5].union(input_sets[i]))==7:
            sets[0] = input_sets[i]
        else:
            assert input_sets[i]==sets[9]

    mapping = {sets[i]:i for i in range(10)}

    out_digits = [mapping[frozenset(o)] for o in out]
    output = int("".join(map(str, out_digits)))
    output_numbers.append(output)

print(output_numbers)
print(sum(output_numbers))

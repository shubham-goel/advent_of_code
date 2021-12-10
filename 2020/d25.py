import numpy as np
from tqdm import tqdm

# file = '2020/inputs/d25.txt'


# # Read the file
# with open(file) as f:
#     lines = [line.strip() for line in f if line.strip()]


def transform(n, loop_size):
    # v = 1
    # for _ in range(loop_size):
    #     v = v*n % 20201227
    # return v
    return pow(n, loop_size, 20201227)

CARD_SECRET_LOOP = 3
DOOR_SECRET_LOOP = 3

CARD_PUBLIC = transform(7, CARD_SECRET_LOOP)
DOOR_PUBLIC = transform(7, DOOR_SECRET_LOOP)

DOOR_ENCR = transform(CARD_PUBLIC, DOOR_SECRET_LOOP)
CARD_ENCR = transform(DOOR_PUBLIC, CARD_SECRET_LOOP)
assert DOOR_ENCR == CARD_ENCR


CARD_PUBLIC = 12578151
DOOR_PUBLIC = 5051300

for CARD_SECRET_LOOP in tqdm(range(1, 100000000)):
    if CARD_PUBLIC == transform(7, CARD_SECRET_LOOP):
        print('found CARD_SECRET_LOOP', CARD_SECRET_LOOP)
        break
for DOOR_SECRET_LOOP in tqdm(range(1, 100000000)):
    if DOOR_PUBLIC == transform(7, DOOR_SECRET_LOOP):
        print('found DOOR_SECRET_LOOP', DOOR_SECRET_LOOP)
        break
DOOR_ENCR = transform(CARD_PUBLIC, DOOR_SECRET_LOOP)
CARD_ENCR = transform(DOOR_PUBLIC, CARD_SECRET_LOOP)
assert DOOR_ENCR == CARD_ENCR
print('ENCR', DOOR_ENCR)
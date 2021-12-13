import numpy as np
from pprint import pprint

file = '2020/inputs/d13.txt'

# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]

START = int(lines[0])
buses = [int(x) for x in lines[1].split(',') if x != 'x']
next_arrival = [-(-START//x)*x for x in buses]
wait_time = np.array([x-START for x in next_arrival])
w, i = wait_time.min(), wait_time.argmin()
print(buses[i], w)
print('P1', buses[i]*w)

ll = lines[1].split(',')
locations = [ll.index(str(x)) for x in buses]

## Efficiently generate a solution to the Chinese remainder theorem
from functools import reduce
def chinese_remainder(m, a):
    sum = 0
    prod = reduce(lambda acc, b: acc*b, m)
    for n_i, a_i in zip(m, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod

def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

divisors = buses
remainders = [-x for x in locations]
print('P2', chinese_remainder(divisors, remainders))

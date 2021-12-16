from typing import Dict, List
import numpy as np
from pprint import pprint
from numba import jit

file = '2021/inputs/d16.txt'

# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]

hexa = lines[0]

hex_to_binary = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}
# Convert 0-9 A-F hex string to binary string
binary = ''.join([hex_to_binary[x] for x in hexa])

# print(binary)

def binary_string_to_int(binary_string: str) -> int:
    """
    Converts a binary string to an integer.
    """
    if isinstance(binary_string, str):
        return int(binary_string, 2)
    elif isinstance(binary_string, list):
        return int(''.join(binary_string), 2)

def parse(B):
    # Parse the binary string into a list of ints
    v = binary_string_to_int(B[:3])
    t = binary_string_to_int(B[3:6])
    if t==4:
        num = []
        for i in range(6, len(B), 5):
            num.extend(B[i+1:i+5])
            if B[i] == '0':
                break
        length_parsed = i+5
        num = binary_string_to_int(num)
        content  = num
    else:
        # Operator
        if B[6] == '0':
            length_parsed = 7+15
            total_length_subpackets = binary_string_to_int(B[7:length_parsed])
            content = []
            while length_parsed < (i+total_length_subpackets):
                p, l = parse(B[length_parsed:])
                length_parsed += l
                content.append(p)
            assert length_parsed == (i+total_length_subpackets)
        else:
            length_parsed = 7+11
            num_subpackets = binary_string_to_int(B[7:length_parsed])
            content = []
            for _ in range(num_subpackets):
                p, l = parse(B[length_parsed:])
                length_parsed += l
                content.append(p)
    return (v,t,content), length_parsed

def p1(content):
    v,t,c = content
    if t==4:
        assert isinstance(c, int)
        return v
    else:
        assert isinstance(c, list)
        return v + sum([p1(x) for x in c])

def p2(content):
    v,t,c = content
    if t==4:
        assert isinstance(c, int)
        return c
    else:
        assert isinstance(c, list)
        parts = [p2(x) for x in c]
        if t==0:
            # Sum
            return sum(parts)
        elif t==1:
            # Product
            return np.prod(parts)
        elif t==2:
            # Minimum
            return min(parts)
        elif t==3:
            # Maximum
            return max(parts)
        elif t==5:
            # Greater than
            return 1 if parts[0] > parts[1] else 0
        elif t==6:
            # Less than
            return 1 if parts[0] < parts[1] else 0
        elif t==7:
            # Equal
            return 1 if parts[0] == parts[1] else 0

content, l = parse(binary)
# pprint(content)
print('P1', p1(content))
print('P2', p2(content))

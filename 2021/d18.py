import ast
import copy
from functools import reduce

file = '2021/inputs/d18.txt'

# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]

# Node in binary tree
class Node:
    def __init__(self, level=0, left=None, right=None, parent=None, value=None):
        self.level = level
        self.left = left
        self.right = right
        self.parent = parent
        self.value = value

    def add_level(self, n):
        self.level += n
        if self.left:
            self.left.add_level(n)
        if self.right:
            self.right.add_level(n)

    def magnitude(self):
        if self.value is not None:
            return self.value
        else:
            return 3*self.left.magnitude() + 2*self.right.magnitude()

    def __str__(self, debug=False) -> str:
        if self.value is not None:
            return f'{self.value}' + (f'L{self.level}' if debug else '')
        else:
            return '[' + str(self.left) + ',' + str(self.right) + ']'

    def replace_with_value(self, value):
        n = Node(level=self.level, parent=self.parent, value=value)
        if self.parent.left == self:
            self.parent.left = n
        else:
            self.parent.right = n

    def check(self):
        if self.left is not None:
            assert self.left.parent == self
            assert self.right.parent == self
            assert self.left.level == self.level + 1
            assert self.right.level == self.level + 1
            assert self.value is None
            self.left.check()
            self.right.check()
        else:
            assert self.left is None
            assert self.right is None
            assert self.value is not None

def parse_to_graph(l):
    if isinstance(l, int):
        return Node(value=l, level=0)
    else:
        left = parse_to_graph(l[0])
        right = parse_to_graph(l[1])
        n = Node(left=left, right=right, parent=None)
        left.parent = right.parent = n
        left.add_level(1)
        right.add_level(1)
        return n

def add(a, b):
    a = copy.deepcopy(a)
    b = copy.deepcopy(b)
    a.add_level(1)
    b.add_level(1)
    c = Node(left=a, right=b, parent=None)
    a.parent = c
    b.parent = c
    return reduce_starfish(c)

def flatten(l: Node):
    # Binary tree to list
    if l.left is None:
        return [l]
    else:
        return flatten(l.left) + flatten(l.right)

def reduce_starfish(l):
    # print('reducing...', l)

    while True:
        refined = False

        # Ensure sanity check
        l.check()

        # Check explode
        ff = flatten(l)
        # print(' '.join([str(f) for f in ff]))

        for i, f in enumerate(ff):
            if f.level > 4:
                # Leftmost element with level at least 4
                assert ff[i].parent == ff[i+1].parent
                if i>0:
                    ff[i-1].value += ff[i].value
                if i+2<len(ff):
                    ff[i+2].value += ff[i+1].value

                # Remove the element
                # print('explode', ff[i].level, ff[i].parent.level, ff[i].parent.parent.level)
                ff[i].parent.replace_with_value(0)

                # print('exploded!', l)
                refined = True
                break
        if refined:
            continue

        # Check split
        for i, f in enumerate(ff):
            if f.value >= 10:
                p = f.parent
                is_left = p.left == f
                v = f.value
                new_f = parse_to_graph([v//2, v//2+v%2])
                new_f.add_level(p.level+1)
                new_f.parent = p
                if is_left:
                    p.left = new_f
                else:
                    p.right = new_f
                # print('split!', l)
                refined = True
                break
        if refined:
            continue

        # Break if neither possible
        break
    
    return l

numbers = [ast.literal_eval(l) for l in lines]
numbers = [parse_to_graph(n) for n in numbers]
[print(n) for n in numbers]
[n.check() for n in numbers]

# Add all numbers
final = reduce(lambda a, b: add(a,b), numbers)
print(final)
print('P1', final.magnitude())

# Find maximum of all possible magnitudes
mag_max = 0
for a in numbers:
    for b in numbers:
        if a!=b:
            mag = add(a, b).magnitude()
            if mag > mag_max:
                mag_max = mag
print('P2', mag_max)

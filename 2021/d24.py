import numpy as np
import copy
from functools import lru_cache
from collections import defaultdict
from numba import njit
from itertools import product

file = '2021/inputs/d24.txt'

# Read the file
with open(file) as f:
    lines = [line.strip() for line in f]

def MONAD(inp, lines):
    i = 0
    var = [0,0,0,0]
    for l in lines:
        # print(l)
        op = l[0]
        v = ord(l[1])-ord('w')
        if len(l)>2:
            if l[2] in ['w','x','y','z']:
                b = var[ord(l[2])-ord('w')]
            else:
                b = l[2]
        if op == 'inp':
            print(i, var)
            var[v] = inp[i]
            i += 1
        elif op == 'add':
            var[v] = var[v] + b
        elif op == 'mul':
            var[v] = var[v] * b
        elif op == 'mod':
            var[v] = var[v] % b
        elif op == 'div':
            var[v] = var[v] // b
        elif op == 'eql':
            var[v] = 1 if var[v] == b else 0
    print(i, var)
    return var

def MONAD_expr(lines):
    from sympy import simplify, symbols, Piecewise, Eq, Q, refine
    i = 0
    var = [0,0,0,0]
    assumptions = True
    for _i, l in enumerate(lines):
        # if _i%20 == 0:
        #     print(var)
        # print(l)
        op = l[0]
        v = ord(l[1])-ord('w')
        if len(l)>2:
            if l[2] in ['w','x','y','z']:
                b = var[ord(l[2])-ord('w')]
            else:
                b = l[2]
        if op == 'inp':
            var[v] = symbols(f'a{i}')
            assumptions = assumptions & Q.integer(var[v]) & Q.nonnegative(var[v]-1) & Q.nonpositive(var[v]-9)
            # var = [refine(simplify(v), assumptions) for v in var]
            var = [simplify(refine(simplify(v), assumptions=assumptions)) for v in var]
            print(_i, assumptions)
            print(_i, var)
            # print(_i, var)
            i += 1
        elif op == 'add':
            var[v] = (var[v] + b)
        elif op == 'mul':
            var[v] = (var[v] * b)
        elif op == 'mod':
            var[v] = (var[v] % b)
        elif op == 'div':
            var[v] = (var[v] // b)
        elif op == 'eql':
            # var[v] = (f'Piecewise((1,Eq({var[v]},{b})), (0,True))')
            var[v] = refine(Piecewise((1,Eq(var[v],b)), (0,True)), assumptions=assumptions)
    print(_i, var)
    return var

def MONAD_func(lll):
    statements = [
        "from numba import njit, int32",
        "@njit(int32(" + ','.join(['int32']*14) + "),nogil=True)",
        "def MONAD_jit(a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13):",
        "    w,x,y,z = 0,0,0,0",
    ]
    i = 0
    for l in lll:
        op = l[0]
        if op == 'inp':
            sss = f'    {l[1]} = a{i}'
            i += 1
        elif op == 'add':
            sss = f'    {l[1]} += {l[2]}'
        elif op == 'mul':
            sss = f'    {l[1]} *= {l[2]}'
        elif op == 'mod':
            sss = f'    {l[1]} = {l[1]}%{l[2]}'
        elif op == 'div':
            sss = f'    {l[1]} = {l[1]}//{l[2]}'
        elif op == 'eql':
            sss = f'    {l[1]} = 1 if {l[1]}=={l[2]} else 0'
        statements.append(sss)
    statements.append("    return z")
    return '\n'.join(statements)

lines2 = []
for l in lines:
    l = l.split(' ')
    ll = []
    ll.append(l[0])
    ll.append(l[1])
    if len(l)==3:
        try:
            ll.append(int(l[2]))
        except ValueError:
            ll.append(l[2])
    lines2.append(ll)
def P1_failed_attempt(lines2):
    f = MONAD_func(lines2)
    exec(compile(f, '<string>', 'exec'))
    # MONAD_jit(*[1]*14)

def P1_2():
    ###
    # x1=1; y1=v0+15; z1=y1
    # x2 = 1;               y2 = v1+8;      z2 = z1*26 + y2
    # x3 = 1;               y3 = v2+2;      z3 = z2*26 + y3
    # x4 = (v2-7!=v3);      y4 = (v3+6)*x4; z4 = (z3//26)*(x4 ? 26 : 1) + y4        # = z2
    # x5 = 1;               y5 = v4+13;     z5 = z4*26 + y5
    # x6 = 1;               y6 = v5+4;      z6 = z5*26 + y6
    # x7 = 1;               y7 = v6+1;      z7 = z6*26 + y7
    # x8 = (v6-4!=v7);      y8 = 0;         z8 = z7//26                             # = z6
    # x9 = 1;               y9 = v8+5;      z9 = z8*26 + y9
    # x10 = (v8-2!=v9);     y10 = 0;        z10 = z9//26                            # = z8 = z6
    # x11 = (v5-8!=v10);    y11 = 0;        z11 = z10//26                           # = z5
    # x12 = (v4+3!=v11);    y12 = 0;        z12 = z11//26                           # = z4 = z2
    # x13 = (v1+7!=v12);    y13 = 0;        z13 = z12//26                           # = z1
    # x14 = (v0+4!=v13);    y14 = 0;        z14 = z13//26                           # = 0

    ## Extracted constraints for z=0:
    # v3 = v2-7
    # v7 = v6-4
    # v9 = v8-2
    # v10 = v5-8
    # v11 = v4+3
    # v12 = v1+7
    # v13 = v0+4

    v0 = 5; v13 = v0+4
    v1 = 2; v12 = v1+7
    v2 = 9; v3 = v2-7
    v4 = 6; v11 = v4+3
    v5 = 9; v10 = v5-8
    v6 = 9; v7 = v6-4
    v8 = 9; v9 = v8-2
    biggest = v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13

    v0 = 1; v13 = v0+4
    v1 = 1; v12 = v1+7
    v2 = 8; v3 = v2-7
    v4 = 1; v11 = v4+3
    v5 = 9; v10 = v5-8
    v6 = 5; v7 = v6-4
    v8 = 3; v9 = v8-2
    smallest = v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13

    return biggest, smallest

biggest, smallest = P1_2()
print('biggest', biggest)
MONAD(biggest, lines2)
print('smallest', smallest)
MONAD(smallest, lines2)

biggest = ''.join(map(str, biggest))
print('P1', biggest)
smallest = ''.join(map(str, smallest))
print('P2', smallest)

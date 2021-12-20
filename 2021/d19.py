import ast
import copy
from functools import reduce
import numpy as np
from numba import jit, njit
from itertools import combinations

file = '2021/inputs/d19.txt'

# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]

scanner_reports = []
prev = 0
for i,line in enumerate(lines):
    if i>0 and line.startswith('--- scanner '):
        scanner_reports.append(np.array([ast.literal_eval(l) for l in lines[prev+1:i]]))
        prev = i
scanner_reports.append(np.array([ast.literal_eval(l) for l in lines[prev+1:]]))

for i,scanner in enumerate(scanner_reports):
    print('Scanner {}: {}'.format(i,scanner))

def all_90_degree_rotations_3d():
    # Returns Rs: 24x3x3all rotation matrices from 24 different orientations:
    # facing positive or negative x, y, or z, and considering
    # any of four directions "up" from that facing.

    Rs = []
    # 0-degree rotation
    R0 = np.array([[1,0,0],[0,1,0],[0,0,1]])
    # 90-degree rotation about x axis
    Rx = np.array([[1,0,0],[0,0,-1],[0,1,0]])
    # 90-degree rotation about y axis
    Ry = np.array([[0,0,1],[0,1,0],[-1,0,0]])
    # 90-degree rotation about z axis
    Rz = np.array([[0,-1,0],[1,0,0],[0,0,1]])
    Rs.append(R0)
    Rs.append(Rx)
    Rs.append(Ry)
    Rs.append(Rz)
    Rs = np.stack(Rs, axis=0)
    Rs = np.unique(Rs, axis=0)

    while True:
        # print(Rs.shape)
        new_Rs = list(Rs.copy())
        for r1 in Rs:
            for r2 in Rs:
                new_Rs.append(np.dot(r1,r2))
        new_Rs = np.stack(new_Rs, axis=0)
        new_Rs = np.unique(new_Rs, axis=0)
        if new_Rs.shape[0] == Rs.shape[0]:
            break
        Rs = new_Rs

    return Rs

def intersect_rows(A,B):
    nrows, ncols = A.shape
    dtype={'names':['f{}'.format(i) for i in range(ncols)],
        'formats':ncols * [A.dtype]}

    C = np.intersect1d(A.view(dtype), B.view(dtype), assume_unique=True)

    # This last bit is optional if you're okay with "C" being a structured array...
    C = C.view(A.dtype).reshape(-1, ncols)
    return C

def try_align(scan1_og, scan2_og, Rs):
    best_C = 0
    for R in Rs:
        # print(R)
        # Attempt aligning scan1[i] to scan2[j]
        for i in range(scan1_og.shape[0]):
            for j in range(scan2_og.shape[0]):
                scan1 = scan1_og.copy()
                scan2 = np.dot(scan2_og, R)
                scan1 = scan1 - (trans1 := scan1[i])
                scan2 = scan2 - (trans2 := scan2[j])
                C = intersect_rows(scan1, scan2)
                best_C = max(best_C, C.shape[0])
                if C.shape[0] >= 12:
                    # At least 12 beacons align. Merge the 2 scans.
                    print(C.shape[0], 'beacons align')
                    scan_merged = np.concatenate((scan1 + trans1, scan2 + trans1), axis=0)
                    scan_merged = np.unique(scan_merged, axis=0)
                    return True, scan_merged, R, trans1-trans2
    print(best_C, 'beacons align')
    return False, None, None, None

def align_all_scans(scanner_reports):
    Rs = all_90_degree_rotations_3d()
    aligned_scans = [s.copy() for s in scanner_reports]
    scanner_positions = [{i:np.array([[0,0,0]])} for i,s in enumerate(scanner_reports)]
    fail_count = [0]*len(scanner_reports)

    while len(aligned_scans) > 1:
        flag = False

        # Sort scans by length to speeed up matching. Scans that failed alignment are less preferred.
        aligned_scans, fail_count = list(map(list, zip(*sorted(zip(aligned_scans, fail_count), key=lambda x: x[0].shape[0] - x[1], reverse=True))))

        for i1,i2 in combinations(range(len(aligned_scans)), 2):
            print('Trying to align {} and {} / {}'.format(i1,i2, len(aligned_scans)), end='... ')
            i1, i2 = min(i1, i2), max(i1, i2)
            s1 = aligned_scans[i1]
            s2 = aligned_scans[i2]
            p1 = scanner_positions[i1]
            p2 = scanner_positions[i2]
            flag, s, R, t = try_align(s1, s2, Rs)
            if flag:
                aligned_scans.pop(i2), scanner_positions.pop(i2), fail_count.pop(i2)
                aligned_scans.pop(i1), scanner_positions.pop(i1)
                aligned_scans.insert(0, s), scanner_positions.insert(0, {**p1, **{k: np.dot(v, R) + t for k,v in p2.items()}})
                break
            else:
                fail_count[i2] += len(s2)
        if not flag:
            raise Exception('No more alignments possible')
    return aligned_scans[0], scanner_positions[0]

s, p = align_all_scans(scanner_reports)
print(s)
print(p)
print('P1', s.shape[0])

def max_manhattan_distance(p):
    # Find maximum manhattan distance between 2 points in a set of points
    # p: Nx3 array of points
    # Returns: max_dist
    max_dist = 0
    for i in range(p.shape[0]):
        for j in range(i+1, p.shape[0]):
            max_dist = max(max_dist, np.abs(p[i]-p[j]).sum())
    return max_dist

p = np.array(list(p.values()))
print('P2', max_manhattan_distance(p))

import numpy as np
from functools import reduce
from collections import defaultdict
from pprint import pprint

file = '2021/inputs/d12.txt'


# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]

edges = [line.split('-') for line in lines]
adj_list = defaultdict(list)
for e in edges:
    adj_list[e[0]].append(e[1])
    adj_list[e[1]].append(e[0])
caves = set(adj_list.keys())
START = 'start'
END = 'end'
is_big = lambda x: (x not in [START, END]) and x[0].isupper()


def add0(s, v):
    if v in s:
        return False
    else:
        s.add(v)
        return True

def bfs(graph, node):
    visited = []    # List to keep track of visited nodes.
    queue = set()   # Initialize a queue
    paths = defaultdict(set)

    visited.append(node)
    queue.add(node)
    paths[node].add(node)

    while queue:
        s = queue.pop()
        # print (s, end = " ")

        curr_paths = [(p.split('-'), p) for p in paths[s]]

        for neighbour in graph[s]:
            for p, p_og in curr_paths:
                if is_big(neighbour) or neighbour not in p:
                    if add0(paths[neighbour], p_og + ('-' + neighbour)):
                        queue.add(neighbour)
    return visited, paths

# Driver Code
visited, paths = bfs(adj_list, START)

print('paths')
pprint(paths[END])
pprint('P1', len(paths[END]))

# Part 2
def bfs2(graph, node, special_small):
    visited = []    # List to keep track of visited nodes.
    queue = set()   # Initialize a queue
    paths = defaultdict(set)

    visited.append(node)
    queue.add(node)
    paths[node].add(node)

    while queue:
        s = queue.pop()
        # print (s, end = " ")

        curr_paths = [(p.split('-'), p) for p in paths[s]]

        for neighbour in graph[s]:
            for p, p_og in curr_paths:
                c = p.count(neighbour)
                if is_big(neighbour)  or c==0 or (neighbour == special_small and c<=1):
                    if add0(paths[neighbour], p_og + ('-' + neighbour)):
                        queue.add(neighbour)
    return visited, paths

small_caves = {x for x in caves if (x not in [START, END]) and x[0].islower()}
paths_final = set.union(*[bfs2(adj_list, START, sc)[1][END] for sc in small_caves])
pprint('P2', len(paths_final))

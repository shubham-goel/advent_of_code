import re
import numpy as np
from collections import defaultdict

file = '2020/inputs/d24.txt'


# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]

directions = ['e', 'ne', 'se', 'w', 'sw', 'nw']
directions = {x:i for i,x in enumerate(directions)}
def parse(path):
    ss = re.split('(n.|s.|e|w)', path)
    return [s for s in ss if s]
def get_tile(path):
    dirs = parse(path)
    dirs = np.array(list(map(lambda x:directions[x], dirs)))
    numE = np.sum(dirs == 0) - np.sum(dirs == 3)
    numNE = np.sum(dirs == 1) - np.sum(dirs == 4) + numE
    numSE = np.sum(dirs == 2) - np.sum(dirs == 5) + numE
    tile = (numNE, numSE)
    return tile

tile_flips = defaultdict(lambda: 0)
# dirs = parse('ewseswnww')
for line in lines:
    tile = get_tile(line)
    tile_flips[tile] += 1

def count_flipped(tile_flips):
    counter = 0
    for tile, count in tile_flips.items():
        if count%2==1:
            counter += 1
    return counter

print(count_flipped(tile_flips))


## Part2
def tile_to_path(tile):
    return 'ne'*tile[0] + 'se'*tile[1]
def tile_to_adj(tile):
    ne,se = tile
    return [
        (ne+1, se),
        (ne, se+1),
        (ne+1, se+1),
        (ne-1, se),
        (ne, se-1),
        (ne-1, se-1),
    ]
def get_tile_adjblack(tile_flips):
    tile_adjblack = defaultdict(lambda: 0)
    for tile, count in tile_flips.items():
        if count%2==1:
            # Tile is black. Increase counter of adj tiles
            adj_tiles = tile_to_adj(tile)
            for tile2 in adj_tiles:
                tile_adjblack[tile2] += 1
    return tile_adjblack

for day in range(100):
    tile_adjblack = get_tile_adjblack(tile_flips)
    tile_flips_new = defaultdict(lambda: 0)

    for tile, adj in tile_adjblack.items():
        if tile_flips[tile]%2==1:
            # Tile is black.
            # Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
            if not(adj == 0 or adj > 2):
                tile_flips_new[tile] = 1    # Stays black
        else:
            # Tile is white.
            # Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
            if adj==2:
                tile_flips_new[tile] = 1    # Fliip to black

    tile_flips = tile_flips_new

print(count_flipped(tile_flips))

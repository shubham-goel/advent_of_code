import numpy as np
import copy
from functools import lru_cache

file = '2021/inputs/d23.txt'

# Read the file
with open(file) as f:
    lines = [line for line in f]

m = {'A':0, 'B':1, 'C':2, 'D':3}

ROOM_SIZE = len(lines)-3
rooms = [
    [m[lines[2+i][3]] for i in range(ROOM_SIZE)],  # @2
    [m[lines[2+i][5]] for i in range(ROOM_SIZE)],  # @4
    [m[lines[2+i][7]] for i in range(ROOM_SIZE)],  # @6
    [m[lines[2+i][9]] for i in range(ROOM_SIZE)],  # @8
]
room_positions = [2, 4, 6, 8]
type_scores = [1, 10, 100, 1000,]
hallway = [None]*11

rooms = tuple(tuple(x) for x in rooms)
hallway = tuple(hallway)

@lru_cache(maxsize=None)
def get_all_valid_moves(rooms, hallway):
    hallway_empty = [x is None for x in hallway]
    moves = []

    for i,k in enumerate(hallway):
        if k is not None:
            j = room_positions[k]
            # Is i -> j clear in hallway?
            clear = all((hallway[x] is None or x==i) for x in range(min(i,j), max(i,j)+1))

            # Is room k occupied properly?
            occ0 = [rooms[k][i] is not None for i in range(ROOM_SIZE)]
            occupied_correctly = True
            for ri in range(ROOM_SIZE):
                if occ0[ri] and rooms[k][ri]!=k:
                    occupied_correctly = False
                    break
            pos = 0
            while pos<ROOM_SIZE and not occ0[pos]:
                pos += 1
            if clear and occupied_correctly and pos >= 0:
                moves.append(['i', i, k, pos-1])

    if len(moves) == 0:
        # Consider out moves only if no in moves are possible
        for k in [0,1,2,3]:
            room_pos = room_positions[k]
            target_positions = []
            for pos in [0,1,3,5,7,9,10]:
                if all(hallway_empty[min(pos, room_pos) : max(pos, room_pos)+1]):
                    target_positions.append((abs(pos-room_pos), pos))
            target_positions = [x[1] for x in sorted(target_positions)]

            first_occupied = 0
            while first_occupied < ROOM_SIZE and rooms[k][first_occupied] is None:
                first_occupied += 1
            if first_occupied < ROOM_SIZE and any(rooms[k][x]!=k for x in range(first_occupied, ROOM_SIZE)):
                [moves.append(['o', k, first_occupied, pos]) for pos in target_positions]
            # occ0 = (rooms[k][0] is not None)
            # occ1 = (rooms[k][1] is not None)
            # if (occ0 and rooms[k][0] != k) or (occ0 and occ1 and rooms[k][1] != k):
            #     [moves.append(['o', k, 0, pos]) for pos in target_positions]
            # if (not occ0 and occ1 and rooms[k][1] != k):
            #     [moves.append(['o', k, 1, pos]) for pos in target_positions]

    return moves

def check_final(rooms, hallway):
    for k in [0,1,2,3]:
        if not (rooms[k][0]==k and rooms[k][1]==k):
            return False
    for h in hallway:
        if h is not None:
            return False
    return True

# DEBUG = True
# WAIING_FOR_MOVE = 0, ['o', 'C', 0, 3]
# WAIING_FOR_MOVE = 1, ['o', 'B', 0, 5]
# WAIING_FOR_MOVE = 2, ['i', 5, 'C', 0]
# WAIING_FOR_MOVE = 3, ['o', 'B', 1, 5]
# WAIING_FOR_MOVE = 4, ['i', 3, 'B', 1]
# WAIING_FOR_MOVE = 5, ['o', 'A', 0, 3]
# WAIING_FOR_MOVE = 6, ['i', 3, 'B', 0]
# WAIING_FOR_MOVE = 7, ['o', 'D', 0, 7]
# WAIING_FOR_MOVE = 8, ['o', 'D', 1, 9]
# WAIING_FOR_MOVE = 9, ['i', 7, 'D', 1]
# WAIING_FOR_MOVE = 10, ['i', 5, 'D', 0]
# WAIING_FOR_MOVE = 11, ['i', 9, 'A', 0]
@lru_cache(maxsize=None)
def do_move(rooms, hallway, score = 0, num_moves = 0, best_score = float('inf')):
    # Iterate over all possible moves
    moves = get_all_valid_moves(rooms, hallway)

    if len(moves) == 0:
        if check_final(rooms, hallway):
            return score
        else:
            return float('inf')

    next_scores = []
    for move in moves:
        # global DEBUG
        # global WAITING_FOR_MOVE
        # if DEBUG and num_moves == WAIING_FOR_MOVE[0] and move == WAIING_FOR_MOVE[1]:
        #     xxx = 0
        rooms_next = list(list(x) for x in rooms)
        hallway_next = list(hallway)

        best_score_next = best_score if len(next_scores)==0 else min(best_score, min(next_scores))
        if move[0] == 'o':
            # moving out of room
            room, rp, hp = move[1], move[2], move[3]
            elem = rooms_next[room][rp]
            curr_score = score + type_scores[elem] * (abs(room_positions[room] - hp) + rp + 1)
            rooms_next[room][rp] = None
            hallway_next[hp] = elem
            if len(next_scores) > 0 and curr_score > best_score:
                next_score = curr_score
            else:
                rooms_next = tuple(tuple(x) for x in rooms_next)
                hallway_next = tuple(hallway_next)
                next_score = do_move(rooms_next, hallway_next, curr_score, num_moves=num_moves+1, best_score=best_score_next)
        elif move[0] == 'i':
            # moving into room
            hp, room, rp = move[1], move[2], move[3]
            assert(hallway[hp] == room)
            curr_score = score + type_scores[room] * (abs(hp - room_positions[room]) + rp + 1)
            rooms_next[room][rp] = room
            hallway_next[hp] = None
            if len(next_scores) > 0 and curr_score > best_score:
                next_score = curr_score
            else:
                rooms_next = tuple(tuple(x) for x in rooms_next)
                hallway_next = tuple(hallway_next)
                next_score = do_move(rooms_next, hallway_next, curr_score, num_moves=num_moves+1, best_score=best_score_next)

        if next_score != float('inf'):
            next_scores.append(next_score)

    return min(next_scores) if len(next_scores) > 0 else float('inf')

score = do_move(rooms, hallway)
print('P1', score)

import numpy as np

file = '2021/inputs/d4.txt'


# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]

called = np.array([int(x) for x in lines[0].split(',')])
lines = lines[1:]

boards = []
assert len(lines) % 5 == 0
for i in range(len(lines) // 5):
    board = [list(map(int, line.split())) for line in lines[i * 5: (i + 1) * 5]]
    boards.append(board)
boards = np.array(boards)
print(boards.shape)

## Part 1
boards1 = boards.copy()
for curr in called:
    boards1[boards1==curr] = -1    # Mark the called number
    aa,bb = np.where(boards1.sum(axis=1) == -5)   # Check if the board is solved
    if len(aa) > 0:
        solved_board_id = aa[0]
        break
    aa,bb = np.where(boards1.sum(axis=2) == -5)   # Check if the board is solved
    if len(aa) > 0:
        solved_board_id = aa[0]
        break

solved_board = np.where(boards1[solved_board_id]==-1, 0, boards1[solved_board_id])
print(solved_board)
print(solved_board.sum() * curr)

## Part 2
boards1 = boards.copy()
solved = np.zeros(boards1.shape[0])
solved_prev = solved.copy()

for curr in called:
    boards1[boards1==curr] = -1    # Mark the called number
    aa,bb = np.where(boards1.sum(axis=1) == -5)   # Check if the board is solved
    solved[aa] = 1

    aa,bb = np.where(boards1.sum(axis=2) == -5)   # Check if the board is solved
    solved[aa] = 1

    # Break if all boards are solved
    if solved.sum() == solved.size:
        last_solved_board = np.where((solved==1) & (solved_prev==0))
        break

    solved_prev = solved.copy()
solved_board = np.where(boards1[last_solved_board]==-1, 0, boards1[last_solved_board])
print(solved_board)
print(curr)
print(solved_board.sum() * curr)

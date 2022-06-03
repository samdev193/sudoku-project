import random
import time
from random import randrange, randint

random.seed(time.time())

# checks if position on board has a number
def is_valid(board: list, pos:tuple, num: int) -> bool:
    #column
    for i in range(0,9):
        if board[pos[0]][i] == num and pos[1] != i:
            return False
    #row
    for i in range(0,9):
        if board[i][pos[1]] == num and pos[0]!= i:
            return False

    # boxes
    box_x = (pos[1]//3) * 3
    box_y = (pos[0]//3) * 3
    for i in range(box_y,box_y + 3):
        for j in range(box_x, box_x + 3):
            if board[i][j] == num and (i,j) != pos:
                return False

    return True

# looks for empty area.
def find_empty(board: list) -> tuple:
    for i in range(0,9):
        for j in range(0,9):
            if board[i][j] == 0:
                return (i,j)  # row, col
    # 0 is not found
    return None

def solve(board: list) -> bool:
    find = find_empty(board)
    # solution found
    if not find:
        return True

    else:
        row, col = find

    for i in range(1,10):
        if is_valid(board, (row, col), i):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0

    return False

def random_board(board):
    fill_matrix(board)
    solve(board)
    remove_digits(board)

# removes random digits on board so it can be solved.
def remove_digits(board: list):
    count = randint(36,46) # number of digits that will be removed

    while count != 0:
        i = randrange(9)
        j = randrange(9)
        if(board[i][j] != 0):
            board[i][j] = 0
        count -= 1

# diagonally fills 3x3 matrix so board can have a valid solution when solve is called.
def fill_matrix(board: list):
    for i in range(9):
        for j in range(9):
            if i < 3 and j < 3:
                num = randint(1, 9)
                while not is_valid(board,(i,j),num):
                    num = randint(1, 9)
                board[i][j] = num

            elif 3 <= i < 6 and 3 <= j < 6:
                num = randint(1, 9)
                while not is_valid(board, (i, j), num):
                    num = randint(1, 9)
                board[i][j] = num

            elif 6 <= i < 9 and 6 <= j < 9:
                num = randint(1, 9)
                while not is_valid(board, (i, j), num):
                    num = randint(1, 9)
                board[i][j] = num


def find_empty(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return r, c
    return None


def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num:
            return False
        if board[i][col] == num:
            return False

    box_row = (row // 3) * 3
    box_col = (col // 3) * 3

    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False

    return True


def solve(board):
    find = find_empty(board)
    if not find:
        return True

    row, col = find

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num

            if solve(board):
                return True

            board[row][col] = 0

    return False
import random

def generate_full_board():
    board = [[0 for _ in range(9)] for _ in range(9)]
    solve_random(board)
    return board


def solve_random(board):
    find = find_empty(board)
    if not find:
        return True

    row, col = find
    numbers = list(range(1, 10))
    random.shuffle(numbers)

    for num in numbers:
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_random(board):
                return True
            board[row][col] = 0

    return False


def remove_numbers(board, difficulty="medium"):
    if difficulty == "easy":
        removals = 35
    elif difficulty == "hard":
        removals = 55
    else:
        removals = 45  # medium

    while removals > 0:
        r = random.randint(0, 8)
        c = random.randint(0, 8)
        if board[r][c] != 0:
            board[r][c] = 0
            removals -= 1

    return board

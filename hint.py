from solver import solve


def get_hint(board):
    copy_board = [row[:] for row in board]

    if not solve(copy_board):
        return None

    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return r, c, copy_board[r][c]

    return None

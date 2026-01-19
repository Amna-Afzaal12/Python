import math
import random
from collections import OrderedDict

PLAYER = "X"
OPPONENT = "O"
EMPTY = " "

WIN_LINES = [
    (0,1,2),(3,4,5),(6,7,8),
    (0,3,6),(1,4,7),(2,5,8),
    (0,4,8),(2,4,6)
]

def winner(board):
    for a,b,c in WIN_LINES:
        if board[a] == board[b] == board[c] != EMPTY:
            return board[a]
    return None

def terminal(board):
    return winner(board) or EMPTY not in board

def utility(board):
    w = winner(board)
    if w == PLAYER:
        return 1
    if w == OPPONENT:
        return -1
    return 0

def moves(board):
    return [i for i,c in enumerate(board) if c == EMPTY]

def make_move(board, i, p):
    b = list(board)
    b[i] = p
    return tuple(b)

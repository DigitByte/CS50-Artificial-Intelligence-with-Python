"""
Tic Tac Toe implementation with Minimax AI
"""

import math
import copy

# Game constants
X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
Returns starting state of the board (3x3 grid of EMPTY).
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
Determines whose turn it is based on board state.
X moves first, then alternates with O.
    """
    is_even = True
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] != EMPTY:
                is_even = not is_even
    return X if is_even else O

def actions(board):
    """
Returns set of all possible (row, col) moves available.
    """
    possible_actions = set()
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == EMPTY:
                possible_actions.add((row, col))
    return possible_actions

def result(board, action):
    """
Returns new board state after making a move.
Validates action and raises exceptions for invalid moves.
    """
    if action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2:
        raise Exception("Invalid coordinates")
    elif board[action[0]][action[1]] != EMPTY:
        raise Exception("Position already occupied")

    new_board = copy.deepcopy(board)
    player_turn = player(new_board)
    new_board[action[0]][action[1]] = player_turn
    return new_board

def winner(board):
    """
Checks all rows, columns, and diagonals for a winner.
Returns X, O, or None if no winner yet.
    """
    # Check rows and columns
    for i in range(3):
        if board[i][0] != EMPTY and board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
        if board[0][i] != EMPTY and board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]

    # Check diagonals
    if board[0][0] != EMPTY and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] != EMPTY and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    return None

def terminal(board):
    """
Determines if game is over (win or full board).
    """
    if winner(board) is not None:
        return True

    for row in board:
        if EMPTY in row:
            return False
    return True

def utility(board):
    """
Returns game outcome score:
1 for X win, -1 for O win, 0 for tie.
    """
    result = winner(board)
    if result == X:
        return 1
    elif result == O:
        return -1
    return 0

def minimax(board):
    """
Implements Minimax algorithm to find optimal move.
Uses recursive helper functions max_value and min_value.
    """
    def max_value(board):
        if terminal(board):
            return (utility(board), None)

        value = float('-inf')
        best_action = None
        for action in actions(board):
            new_board = result(board, action)
            new_value = min_value(new_board)[0]
            if new_value > value:
                value = new_value
                best_action = action
        return (value, best_action)

    def min_value(board):
        if terminal(board):
            return (utility(board), None)

        value = float('inf')
        best_action = None
        for action in actions(board):
            new_board = result(board, action)
            new_value = max_value(new_board)[0]
            if new_value < value:
                value = new_value
                best_action = action
        return (value, best_action)

    current_player = player(board)
    if current_player == X:
        return max_value(board)[1]
    else:
        return min_value(board)[1]
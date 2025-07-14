"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None



def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    if board == initial_state:
        return X
    
    counterX = 0
    counterO = 0

    for row in board:
        for column in row:
            if column == X:
                counterX+=1
            elif column == O:
                counterO+=1

    if counterX==counterO or counterO>counterX:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    actions = set()

    for i,row in enumerate(board):
        for j,column in enumerate(row):
            if column == EMPTY:
                action = (i,j)
                actions.add(action)

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    i,j = action
    p = player(board)
    new_board = [row[:] for row in board]

    new_board[i][j] = p

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    val = utility(board)

    if val == 1:
        return X
    elif val == -1:
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    counter = 0
    for i in board:
        for j in i:
            if j == X or j == O:
                counter+=1

    if counter == 9:
        return True
    elif utility(board) != 0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    winner = EMPTY
    
    #for rows
    for i in range(len(board)):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            winner = board[i][0]
            break
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            winner = board[0][i]
            break

    #for diagonals
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        winner = board[1][1]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        winner = board[1][1]

    if winner == X:
        return 1
    elif winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """ 

    if terminal(board):
        return utility(board)

    actions_dict = {}
    p = player(board)
    avalible_actions = actions(board)

    for action in avalible_actions:
        value = minimax2(result(board, action))
        actions_dict[action] = value

    if p == X:
        return max(actions_dict, key=actions_dict.get)
    else:
        return min(actions_dict, key=actions_dict.get)

def minimax2(board):
    if terminal(board):
        return utility(board)

    actions_dict = {}
    p = player(board)

    avalible_actions = actions(board)

    if p == X:

        for action in avalible_actions:
            value = minimax2(result(board, action))
            actions_dict[action] = value
        best_move = max(actions_dict, key=actions_dict.get)
        return actions_dict[best_move]
    else:

        for action in avalible_actions:
            value = minimax2(result(board, action))
            actions_dict[action] = value
        best_move = min(actions_dict, key=actions_dict.get)
        return actions_dict[best_move]
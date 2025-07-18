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

    # if the bpaard is in initail state then its X's turn(first turn)
    if board == initial_state:
        return X

    # counter for X and O in board
    counterX = 0
    counterO = 0

    # loop that runs and counts the elements
    for row in board:
        for column in row:
            if column == X:
                counterX += 1
            elif column == O:
                counterO += 1

    # if the number of X and O is same then its X's turn otherwise it is O's turn
    if counterX == counterO or counterO > counterX:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # actions is a set of action
    actions = set()

    # this loop runs adn puts action if it is empty
    for i, row in enumerate(board):
        for j, column in enumerate(row):
            if column == EMPTY:
                action = (i, j)
                actions.add(action)

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # extracting the pair of ints from the action
    i, j = action
    p = player(board)
    new_board = [row[:] for row in board]
    # copying the board so it doesnt cause main board to change

    # raises exception if move already taken or the value is out of bound
    if new_board[i][j] != EMPTY or (i > 2 or i < 0) or (j > 2 or j < 0):
        raise Exception
    else:
        new_board[i][j] = p

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    val = utility(board)  # to get the value 1,0,-1

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
                counter += 1

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

    # for rows
    for i in range(len(board)):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            winner = board[i][0]
            break
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            winner = board[0][i]
            break

    # for diagonals
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

    if terminal(board):  # if the board is already complete then we return none
        return None

    actions_dict = {}  # actions dictionary store action(i,j) with a value by utility()
    p = player(board)  # for geting the turn
    avalible_actions = actions(board)  # for getting all the empty (i,j)

    '''there are two layers
       the outer layer minimax() and the inner layer minimax2()
       reason being that the outer layer returns tuple but the inner layer returns value
       value is utility when the board is complete'''

    for action in avalible_actions:  # runs for outer layer of the minimax
        value = minimax2(result(board, action))  # runs the inner layer
        actions_dict[action] = value  # saves the value against the move(key)

    if p == X:  # returns maximum if the ai was turning for X and minimum if it was turning for O
        return max(actions_dict, key=actions_dict.get)
    else:
        return min(actions_dict, key=actions_dict.get)


def minimax2(board):  # inner layer
    if terminal(board):  # when the board is complete we return the utility value
        return utility(board)

    actions_dict = {}  # same use as outer layer
    p = player(board)  # get the current player(X or O)

    avalible_actions = actions(board)  # same use as outer layer

    '''now the inner layer runs recursively until it is terminal()->True
       if the turn starts with X it will play the moves from avalible_actions
       p==X will run for the maxinmum and call the p==O in the recursion to check what the opponent will play
       this will keep returning back and we will have a value for a move on the outer layer(1,0,-1)

       max() and min() work like this

       actions_dict can be {(0,1):1,(0,2):0}
       they will retrieve the tuple that is the key to the value that is maximum or minimum

       and we return the value because this is the inner layer

       in the outer layer we return the key(tuple) itself'''

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

#import math

EMPTY = None
O = 'O'
X = 'X'

board = [[EMPTY, X, X],
        [EMPTY, EMPTY, O],
        [O, EMPTY, "X"]]



import tictactoe as titit

'''for i in titit.actions([['X', 'X', 'X'],
                        ['X', 'X', EMPTY],
                        ['X', 'X', 'X']]):
    print(i)'''

'''new_dict = {(0,2):1, (0,1):0,(0,0):-1}
new_dict[(1,2)] = 1

print(new_dict)'''

print(titit.terminal(board))
print(titit.player(board))
print(titit.minimax(board))
print(board)
from minesweeper import *

s = Sentence({(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)}, 2)

s.mark_mine((1,2))

print(s.cells)
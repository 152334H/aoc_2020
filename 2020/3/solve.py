from aoc import *
s = sread('input', str, '\n')
grid = makeGrid(s, xmax:=len(s[0]), ymax:=len(s))
def traverse(right,down):
    return sum(grid[((y*right//down)%xmax,y)]=='#' for y in range(0,ymax,down))
print(traverse(3,1))
print(prod(traverse(*t) for t in [(r,1) for r in range(1,8,2)]+[(1,2)]))

from aoc import *
grid = makeGrid(s:=sread('input', str, '\n'), xmax:=len(s[0]), ymax:=len(s))
traverse = lambda R,D: sum(grid[((y*R//D)%xmax,y)]=='#' for y in range(0,ymax,D))
print(traverse(3,1))
print(prod(traverse(*t) for t in [(r,1) for r in range(1,8,2)]+[(1,2)]))

from aoc import *
from re import findall
s = sread('input',str,'\n\n')
def borders(grid, xma=10, yma=10):
    # note that all grids have 4 different borders.
    # N E S W
    return [''.join(grid[(x,0)] for x in range(xma)),
            ''.join(grid[(xma-1,y)] for y in range(yma)),
            ''.join(grid[(x,yma-1)] for x in range(xma)),
            ''.join(grid[(0,y)] for y in range(yma)),
            ]
def parse(lines):
    num, *grid = lines.strip().split('\n')
    xma, yma = len(grid[0]), len(grid)
    grid = makeGrid(grid)
    num = int(findall('[0-9]+', num)[0])
    return num,grid

s = [parse(lines) for lines in s]
grids = dict(s)
has_border = dd(lambda: []) # border, num
num_to_borders = {}
for num,grid in s:
    num_to_borders[num] = borders(grid)
    for b in num_to_borders[num]:
        has_border[b].append(num)
        has_border[b[::-1]].append(num)
print(prod(num for num,grid in s if sum(1 for b in borders(grid) if len(has_border[b]) == 1) == 2))

fullgrid = dd(lambda: '?')
# we'll "just" BFS from a random subgrid
def flipx(grid,xma=10,yma=10): return dict(((xma-1-x,y),grid[x,y]) for x in range(xma) for y in range(yma))
def flipy(grid,xma=10,yma=10): return dict(((x,yma-1-y),grid[x,y]) for x in range(xma) for y in range(yma))
def flipaxis(grid, axis, xma=10,yma=10): return [lambda *d:d[0], flipx, flipy][axis](grid,xma,yma) # 0 is nothing, 1 is x, -1 is y.
def remove_border(grid, xma=10, yma=10): return dict(((x-1,y-1),grid[(x,y)]) for x in range(1,xma-1) for y in range(1,yma-1))
def rotate(grid, xma=10, yma=10):# rotates clockwise by 90deg
    return dict(((yma-1-y,x),grid[(x,y)]) for x in range(0,xma) for y in range(0,yma))
def newadj(x,y,r=8): return Map(lambda p: pmul(p,r), [(0,-1), (1,0), (0,1), (-1,0)])
queue = [(s[0][0],0,0,0,0)]
seen = set()
while queue:
    neq = []
    for num,x,y,angle,flip in queue:
        if num in seen: continue
        seen.add(num)
        # preproc grid
        grid = grids[num]
        for _ in range(angle): grid = rotate(grid)
        grid = flipaxis(grid,flip)
        # loop over all adjacent subgrids
        for b in num_to_borders[num]: 
            if len(has_border[b]) != 2: continue # this is an edge-border
            other_num = next(n for n in has_border[b] if n != num)
            if other_num in seen: continue
            # big terrible processing
            def index2(ls,a,b): # try indexing both values
                return ls.index(a) if a in ls else ls.index(b)
            direct = index2(borders(grid), b, b[::-1]) #(rot+angle) % 4
            other_direct = index2(num_to_borders[other_num], b, b[::-1])
            other_needed_direct = (direct + 2) % 4
            amt_to_rotate = (other_needed_direct - other_direct) % 4 # e.g. 1-2 --> 3
            # should we flip?
            new_flip = 0
            tmp = grids[other_num]
            for _ in range(amt_to_rotate): tmp = rotate(tmp)
            if borders(tmp)[other_needed_direct] != borders(grid)[direct]: # if needds flipping
                new_flip = -1 if other_needed_direct % 2 else 1 # bool(direct%2) --> flip by y.
            neq.append((other_num, *padd((x,y),newadj(x,y)[direct]), amt_to_rotate, new_flip))
        grid = remove_border(grid)
        for p in grid: fullgrid[padd(p,(x,y))] = grid[p] 
    queue = neq
# Now for seamonster counting
xmi,xma,ymi,yma = getGridBoundaries(fullgrid)
fullgrid = dict(((x-xmi,y-ymi),fullgrid[(x,y)]) for x in range(xmi,xma) for y in range(ymi,yma))
xmi,xma,ymi,yma = getGridBoundaries(fullgrid)
def seamonsters(grid):
    SEA_MONSTER = '''                  # \n#    ##    ##    ###\n #  #  #  #  #  #   '''.split('\n')
    sea_monster = makeGrid(SEA_MONSTER)
    sea_monster = dict((p,v) for p,v in sea_monster.items() if v == '#')
    _,sea_xma,_,sea_yma = getGridBoundaries(sea_monster)

    for x in range(xmi,xma-sea_xma+1):
        for y in range(ymi,yma-sea_yma+1):
            if all(grid[padd((x,y),p)] == sea_monster[p] for p in sea_monster):
                for p in sea_monster: grid[padd((x,y),p)] = 'O'
    return sum(map(lambda v: v == 'O', grid.values()))
# I have no idea what the correct orientation is, so let's just try all of them & grab the max.
ma = 0
for flip in range(-1,2):
    fullgrid = flipaxis(fullgrid,flip,xma,yma)
    for direct in range(4):
        xmi,xma,ymi,yma = getGridBoundaries(fullgrid)
        copy = fullgrid.copy()
        if (v:=seamonsters(copy)) > ma: ma = v
        fullgrid = rotate(fullgrid,xma,yma)
print(sum(map(lambda v: v == '#', fullgrid.values()))-ma)

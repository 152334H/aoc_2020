from aoc import *
s,grid = sreadlines('input'), {}    # predefine globalvars

def valid(p): return Valid(p,s) # namespace abuse!
def alladj(p): return Map(lambda p: grid[p], filter(valid, adjdiag(*p)))
def seeadj(p):
    def look(cur, direction):
        while valid(cur := padd(cur, direction)):
            if grid[cur] != '.': yield grid[cur]
        yield '.'
    return [next(look(p,direct)) for direct in adjdiag(0,0)]
def shift(grid, calc_adj, PART2):
    return dict((k, '#' if v == 'L' and calc_adj(k) == 0 else (
                    'L' if v == '#' and calc_adj(k) >= 4+PART2 else v )
                ) for k,v in grid.items())
for part2 in range(2):
    ng = makeGrid(s)
    grid = dict((p,'.') for p in ng)    # dont use a defaultdict
    while not all(ng[k] == grid[k] for k in ng):
        for k in ng: grid[k] = ng[k] 
        ng = shift(grid, lambda k: sum(map(lambda v: v == '#', (alladj,seeadj)[part2](k))), part2)
    print(sum(map(lambda v: v == '#', grid.values())))

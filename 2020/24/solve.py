from aoc import *
DELIMS = {'e' :(1,0),
          'se':(0,1),
          'sw':(-1,1),
          'w' :(-1,0),
          'ne':(1,-1),
          'nw':(0,-1) }
def parse(l): # return tile to be flipped
    skip, rtr = 0, []
    for i,c in enumerate(l[:-1]):
        if skip:
            skip = 0
            continue
        if c+l[i+1] in DELIMS:
            c += l[i+1]
            skip = 1
        rtr.append(DELIMS[c])
    if not skip: rtr.append(DELIMS[l[-1]])
    return reduce(padd,rtr)

grid = dd(lambda: False) # tiles are black (1) or white (0) 
for p in sreadlines('input',parse): grid[p] = not grid[p]
print(sum(grid.values()))

def hadj(p): return [padd(p,t) for t in DELIMS.values()]
def adjv(p): return sum(grid[p] for p in hadj(p))
blacks = set([k for k,v in grid.items() if v]) # tiles to bother looking at
for i in range(100):
    ng,nb = dd(lambda: False), set()
    for p in set(sum([hadj(p) for p in blacks],[]))|blacks:
        if grid[p] and not 0 < adjv(p) <= 2: ng[p] = False
        elif not grid[p] and adjv(p) == 2: ng[p] = True
        else: ng[p] = grid[p]
        if ng[p]: nb.add(p)
    blacks, grid = nb, ng
print(sum(grid.values()))


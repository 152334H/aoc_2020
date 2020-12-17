from aoc import *
s = sreadlines('input')
grid = makeGrid(s)
world3d = World((k+(0,),grid[k]=='#') for k in grid)
world4d = World((k+(0,0),grid[k]=='#') for k in grid)
def active(world,p): return sum(world[p] for p in adjdiagn(*p))

for world in (world3d, world4d):
    for i in range(6):
        newworld = World({(0,)*world.dimen:0})
        for p in world.within_and_adj():
            if world[p]: newworld[p] = 2 <= active(world,p) <= 3
            else: newworld[p] = active(world,p) == 3
        world = newworld
    print(sum(world.values()))

from aoc import *
def parse(l): return (l[0], int(l[1:]))
def rotate(x,y): return (y,-x)
s = sreadlines('input', parse)
MOV, MOVDIR = [(1,0), (0,-1), (-1,0), (0,1)], 'ESWN'
direct, loc = 0, (0,0)
for act,v in s:
    if act in 'LR': direct = (direct+(v//90)*[-1,1][act == 'R']) % 4
    elif act == 'F': loc = padd(loc, pmul(MOV[direct],v))
    elif act in 'NSEW': loc = padd(loc, pmul(MOV[MOVDIR.index(act)],v))
print(sum(map(abs,loc)))

loc, wpt = (0,0), (10,1)
for act,v in s:
    if act in 'LR':
        direct = ((v//90)*[-1,1][act == 'R']) % 4
        for _ in range(direct): wpt = rotate(*wpt)
    elif act == 'F': loc = padd(loc, pmul(wpt,v))
    elif act in 'NSEW': wpt = padd(wpt, pmul(MOV[MOVDIR.index(act)],v))
print(sum(map(abs,loc)))

from collections import defaultdict as dd, Counter
from functools import reduce    # useful
from itertools import * # useful
from math import *  # for prod() and others

# FIXING ITERABLES
Map = lambda f,l: list(map(f,l))
Sorted = lambda l: list(sorted(l))
Filter = lambda f,l: list(filter(f,l))
Reversed = lambda l: list(reversed(l))

def star(f): return lambda args: f(*args)   # lambda tuple unpacking

# MISC ALGOS
def binsearch(f, ma): #thus far, only tested on `ma=2**i`
    '''binary search across an arbitrary function F(x), with a maximal value of MA (and a minimal value of 0)'''
    c = ma
    sign = True
    i = len(bin(ma))-2
    while i:
        i -= 1  #decrease the exponent
        c += [1,-1][sign]*(1<<i)    #increase/reduce c
        sign = f(c) #true/false -> should decrease/increase
    if sign: c-=1 #if binary search ended off-by-one
    return c

def cumsum(ls): return [ls[i+1]+ls[i] for i in range(len(ls)-1)]

def cumsub(ls): return [ls[i+1]-ls[i] for i in range(len(ls)-1)]

# INPUT FUNCS
def sread(name, constructor=str, div=None):
    '''read file NAME, split it with DIV and parse it with a given constructor
    when DIV is given, `constructor()` is mapped over each elem.
    Otherwise, constructor() is used for the entire input.'''
    with open(name) as f: s = f.read()
    if s[-1] == '\n': s = s[:-1]
    if div == None: return constructor(s)
    return Map(constructor, s.split(div))

def sreadlines(name, constructor=str, div=None):
    '''sread, but split across newlines first
    constructor() is used for each element/line if div is given/None'''
    if div is None: return sread(name,constructor,'\n')
    return Map(lambda l: Map(constructor,l.split(div)), sread(name,str,'\n'))

# GRID-RELATED
def makeGrid(s, xma=None, yma=None):
    '''creates a grid of (x,y):val pairs from a sreadlines() string-list
    the default values for xma&yma are len(s[0]) and len(s) respectively.'''
    grid = {}
    for y in range(yma if yma is not None else len(s)):
        for x in range(xma if xma is not None else len(s[0])):
            grid[P([x,y])] = s[y][x]
    return grid
#MAP's default value is an anonymous object with only one property: MAP[v]==v.
def getGridBoundaries(d):
    ''' returns xmi, xma, ymi, yma for a grid.'''
    tl = d.keys()
    yl = [t[1] for t in tl]
    return min(tl)[0], max(tl)[0]+1, min(yl), max(yl)+1
def toGrid(d, MAP=type('',(object,),{'__getitem__':lambda _,v:v})()):
    '''converts a dictionary grid D to a printable representation using the value-to-char mapping MAP
    if MAP is not given, it is assumed that each value of D is a single char'''
    xmi, xma, ymi, yma = getGridBoundaries(d)
    s = ""  # separate this out to make debugging easier.
    for y in range(ymi, yma): # prior: range(yma-1, ymi-1, -1):
        s += ''.join(MAP[d[(x,y)]] for x in range(xmi,xma)) + '\n'
    return s

def adjdiagn(*argc): # all adj+diag points for a point of any dimensions
    return tuple(P(t) for t in adjdiagn_with_self (*argc) if t != argc)

def adjdiagn_with_self(*argc): # all adj/diag points, plus the point itself
    if not len(argc):
        yield ()
        return # i.e. return [()]. 
    for d in range(-1,2):
        for t in adjdiagn_with_self(*argc[1:]):
            yield (argc[0]+d,)+t

def adj(x,y):   # North South East West
    '''returns an array of the 4 (x,y) coordinates adjacent to the input coordinate'''
    return Map(P,[(x,y+1), (x,y-1), (x+1,y), (x-1,y)])

def diag(x,y):
    '''get the 4 points diagonally-adjacent to (x,y),
    starting from the top-right, clockwise'''
    return Map(P,[(x+1,y-1), (x+1,y+1), (x-1,y+1), (x-1,y-1)])

def adjdiag(x,y):
    '''adj(x,y)+diag(x,y)'''
    return adj(x,y)+diag(x,y)

def padd(p1,p2): return tuple(Map(lambda t: t[0]+t[1], zip(p1,p2)))

def pmul(p,v): return tuple(c*v for c in p)

def valid(p, xmi, xma, ymi, yma):
    '''check if a point falls within the given ranges'''
    return  xmi <= p[0] < xma and ymi <= p[1] < yma

def Valid(p, s):
    '''valid(), but grab xma/yma from input lines s[][].'''
    return valid(p, 0, len(s[0]), 0, len(s))

def back_adj(adj_c, i):
    '''given a coordinate from adj(), get back the original (x,y)'''
    return adj(*adj_c)[{0:1, 1:0, 2:3, 3:2}[i]]

def adj(x,y):   # North South East West
    '''returns an array of the 4 (x,y) coordinates adjacent to the input coordinate'''
    return Map(P,[(x,y+1), (x,y-1), (x+1,y), (x-1,y)])

class P(tuple):
    #def __add__(self, other): return P(map(star(lambda a,b:a+b), zip(self,other)))
    def add(self, other): return P(map(star(lambda a,b:a+b), zip(self,other)))
    def __sub__(self, other): return P(map(star(lambda a,b:a-b), zip(self,other)))
    def mul(self, v:int): return P(map(lambda c: c*v, self))

class World(dict): # n-dimensional "grid" that tracks its boundaries 
    def _checkbound(self,p): # to automatically increase the boundaries of the world
        for i,v in enumerate(p):
            if self.mi[i] > v: self.mi[i] = v
            if self.ma[i] <= v: self.ma[i] = v+1
    def __init__(self, *argc, **kwargs): # initialise self.dimen, self.mi, self.ma
        super().__init__(*argc,**kwargs)
        if not len(self): raise ValueError('World() needs at least 1 key-value pair to initialise, sorry!')
        self.dimen = len(next(k for k in self)) # assume all points are same dimen
        self.mi, self.ma = [0]*self.dimen,[0]*self.dimen
        for p in self: self._checkbound(p)
    ## !! this defaults to 0 !!
    def __getitem__(self,p): # in particular, DON'T expand the dictionary
        tile = self.get(p,0) # on unknown keys, unlike defaultdict
        if tile: self._checkbound(p)
        return tile
    def __setitem__(self,p,tile): # use _checkbound if needed.
        if tile: self._checkbound(p)
        super().__setitem__(p,tile)
    def within_and_adj(self):
        '''returns iterator over all points within the world border,
        expanded by +1 on both sides'''
        def recur(i): # recursively get all points for any dimen
            if i == self.dimen:
                yield ()
                return
            for v in range(self.mi[i]-1, self.ma[i]+1):
                for t in recur(i+1): yield (v,)+t
        return recur(0)

def distance_map(start, grid, func, optional=lambda:0):
    '''returns a dict containing a grid's (coord:manhatten-distance-to-start) pairings
    `grid` must be a dict with (x,y) tuples as keys, and with its corresponding traversable values within `walkable`
    `func()` is to determine if a point is legally traversable on the grid
    `optional()` runs once for each point on the grid'''
    from collections import defaultdict as dd
    d = dd(lambda: 0)   #start counting distance from 0
    border = [start]    #an expanding border (coord, traversal-history) of the traversed portion of the grid.
    for coord in border:
        adjacent = adj(*coord)  #list of directly (taxicab) adjacent coordinates
        for direct in range(4): #loop numerically, rather than by *adj(), to provide direction info to func()
            adj_c = adjacent[direct]    #unnecessary variable for clarity
            if adj_c not in d:
                if func(adj_c, grid, direct):
                    border.append(adj_c)    #update border
                    d[adj_c] = d[coord]+1   #add to distance dict
        optional()  #do something after each iteration
    return d

import heapq
class PQ(list):
    def push(self, v):
        return heapq.heappush(self, v)
    def next(self):
        return heapq.heappop(self)

def dijkstra(nodes, edges, cond, deps=dd(lambda:dd(lambda:set())), reachable=lambda *v: True, start='@'):
    '''run dijkstra on `nodes` & `edges`, plus other extra criteria.
    Arguments:
        `nodes`: grid-map (any dict following the format of makeGrid())
        `edges`: a "2d-dict" of {start:{end:distance}} distance maps
        `cond`: a function that determines when dijkstra is finished,
            given `a set() of all node values seen`, as well as `nodes`.
        `deps`: a dict of {node:set(nodes)} pairs.
            Each node in `deps` is "locked" until all of the nodes in
            set(nodes) have been visited. By default, all nodes lack dependents
            Useful for e.g. abstracting doors that require keys
        `reachable`: function that takes in (nodevalue, nodepos),
            returning a bool to indicate if it is ALWAYS traversable.
            Use this if certain tiles on the map are blacklisted/obstacles.
        `start`: the starting node's value.
    Returns:
        The shortest distance found.
    '''
    states = set()  #keeps track of paths traversed
    q = PQ(((0, start, set((start,))),))
    while len(q): #while condition should never break
        moved, self, seen = q.next()
        #verify that current path is new
        check = frozenset(seen|set(['!'+self]))
        if check in states: continue
        states.add(check)   # check can only be added as a frozenset.
        #break if search is finished
        if cond(seen, nodes): break
        #otherwise, branch out
        for k in nodes:
            if k in seen: continue
            if not reachable(self, k): continue
            if deps[self][k].issubset(seen):
                q.push((edges[self][k]+moved, k, seen|set([k])))
    return moved

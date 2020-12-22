from aoc import *
from collections import deque # left is top, right is bottom

def parse(l): return deque(Map(int,l.split('\n')[1:]))
s = sreadlinelines('input', parse)

def round(state, cards, winner=None):
    winner = cards[1] > cards[0] if winner is None else winner # 0 if c1 > c2
    state[winner].append(cards[winner])
    state[winner].append(cards[winner-1])
def score(state):
    winq = state[0] if len(state[0]) else state[1]
    print(sum(prod(t) for t in zip(range(len(winq),0,-1), winq)))

while all(len(q) for q in s): round(s, [q.popleft() for q in s])
score(s)

from itertools import islice
s = sreadlinelines('input', parse)
def recurse(state):
    seen = set()
    def to_hashable(twodeques): return tuple(tuple(q) for q in twodeques)
    while all(len(q) for q in state):
        if (h:=to_hashable(state)) in seen: break
        seen.add(h)
        #
        cards = [q.popleft() for q in state]
        if all(len(state[i]) >= c for i,c in enumerate(cards)):
            newstate = [deque(islice(q,0,cards[i])) for i,q in enumerate(state)]
            winner = recurse(newstate)#...
        else: winner = None
        round(state, cards, winner)
    else: return len(state[0])==0 # if not break
    return 0 # p1 wins if seen()
recurse(s)
score(s)

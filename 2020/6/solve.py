from aoc import *
from operator import __or__, __and__
def parse(s): return Map(frozenset,s.split('\n'))
groups = sread('input', parse, '\n\n')
for op in [__or__, __and__]:
    print(sum(len(reduce(op, g)) for g in groups))

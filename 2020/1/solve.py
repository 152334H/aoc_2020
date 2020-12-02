from aoc import *
s = sread('input', int, '\n')
for i in (2,3):
    print(prod(next(filter(lambda t: sum(t)==2020, combinations(s,i)))))

from re import sub
from aoc import *
class NewInt(int):
    def __sub__(self, other): return NewInt(self*other)
    def __add__(self, other): return NewInt(super().__add__(other))
    def __pow__(self, other): return NewInt(self+other)
def parse1(l): return sub('([0-9]+)', r'NewInt(\1)', l).replace('*','-')
print(sum(eval(l) for l in sreadlines('input', parse1)))
def parse2(l): return parse1(l).replace('+','**')
print(sum(eval(l) for l in sreadlines('input', parse2)))

from aoc import *
def parse_pass(p): return int(''.join(str(int(c in 'BR')) for c in p),2)
passes = sreadlines('input', parse_pass)
mi,ma = min(passes), max(passes)
print(ma)
print(sum(range(mi,ma+1))-sum(passes))

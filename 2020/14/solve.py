from aoc import *
from re import findall
def parse(lines):   # split by mask; this func parses an entire group of writes
    if lines == '': return None # necessary beacuse of sread()
    mask, *writes = lines.strip().split('\n')
    writes = dict(Map(lambda l: map(int,findall('[0-9]+',l)), writes))
    return mask, writes # (mask: str, writes: Dict[int,int])
s = sread('input', parse, 'mask = ')[1:]    # ignore the first None by [1:]
mem = {}
for mask, writes in s:
    for addr,v in writes.items():
        bin_v = bin(v)[2:].rjust(36,'0')
        bits = ''.join(bin_v[i] if b == 'X' else b for i,b in enumerate(mask))
        mem[addr] = int(bits,2)
print(sum(mem.values()))
mem = {}
def writeX(addr, v):
    try:
        first_x = addr.index('X')
        back, fwd = addr[:first_x], addr[first_x+1:]
        for c in '01': writeX(back+c+fwd,v)
    except ValueError: mem[addr] = v #there is no X
for mask, writes in s:
    for addr,v in writes.items():
        baddr = bin(addr)[2:].rjust(36,'0')
        writeX(''.join(b if b!='0' else baddr[i] for i,b in enumerate(mask)),v)
print(sum(mem.values()))

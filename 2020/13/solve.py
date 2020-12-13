from aoc import *
earliest,ids = sreadlines('input')
earliest = int(earliest)
ids = [int(v) if v != 'x' else None for v in ids.split(',')]

def wrongmod(val,mod): return (mod-(val%mod))%mod
print(prod(min((wrongmod(earliest,x),x) for x in ids if x is not None)))

timestamp = 0
LCM = 1
def lcm(x,y): return abs(x*y)//gcd(x,y) # Awaiting py3.9
for i,x in enumerate(ids):
    if x is None: continue
    while (timestamp+i) % x: # while timestamp not working,
        timestamp += LCM     # move up timestamp by one LCM.
    LCM = lcm(LCM,x) # set new LCM
print(timestamp)

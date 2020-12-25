from aoc import *
p = 20201227
s = sreadlines('input', int)
for i in range(1,1000000):
    if pow(7,i,p) in s: break
print(pow(s[s.index(pow(7,i,p))-1],i,p))

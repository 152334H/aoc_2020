from aoc import *
s = sreadlines('input', int)
s+= [0,max(s)+3]
s.sort()
# part 1
diff = cumsub(s)
count = (Counter(diff))
print(count[1]*count[3])
# part 2
ways = dd(int)
ways[s[-1]] = 1
for i in Reversed(s)[1:]:
    ways[i] = ways[i+1]+ways[i+2]+ways[i+3]
print(ways[0])

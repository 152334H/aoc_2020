from aoc import *
s = sread('input', str)
#s = '389125467'
s = [int(c) for c in s]
mi = min(s)
sorted_s = Sorted(s)

def move(cups):
    cur = cups[0]
    three = cups[1:4]
    cups = [cur] + cups[4:]

    for i in range(1,999):
        label_of_dest = sorted_s[sorted_s.index(cur)-i] # 
        try: dest = cups.index(label_of_dest)
        except ValueError: continue
        break
    else: print("PANIC")
    cups = cups[:dest+1] + three + cups[dest+1:]
    
    return cups[1:2]+cups[2:]+cups[0:1]
for i in range(100):
    s = move(s)
    #print(s)
while s[0] != 1:
    s = [*s[1:], s[0]]
print(''.join(map(str,s[1:])))


# probably, if the destination cup wraps around to 1million, we can expect that we'll never see those 3 numbers again.
# hence, we can just throw in numbers as necessary.

s = '389125467'
s = [int(c) for c in s]

class Node(int):
    def __init__(self,v):
        self.next = None
llmap = dict((i,Node(i)) for i in range(10, 1000001))
for v in s: llmap[v] = Node(v)
for i in range(len(s)-1): llmap[s[i]].next = llmap[s[i+1]]
llmap[s[-1]].next = llmap[10]
for i in range(10,1000000): llmap[i].next = llmap[i+1]
llmap[1000000].next = llmap[s[0]]

cups = llmap[s[0]]
def popafter():
    nex = cups.next
    cups.next = nex.next
    return nex
def move(cups):
    three = [popafter() for _ in range(3)]

    dest_lbl = cups-1
    while dest_lbl in three:
        dest_lbl -= 1
        if not dest_lbl: dest_lbl = 1000000
    dest = llmap[dest_lbl]
    aft = dest.next
    for n in three: dest = dest.next = n
    dest.next = aft
    
for i in range(100000000):
    move(cups)
    cups = cups.next
    if i % 100000 == 0: print("hi")
print(llmap[1].next)

from aoc import *
def dowith(ma):
    part1 = ma < 10

    class Node(int):
        def __init__(self,v): self.next = None
    s = Map(int, sread('input', str)) + list(range(10,ma+1))
    llmap = {}
    for i,v in enumerate(s): llmap[v] = s[i] = Node(v)
    for i in range(len(s)-1): s[i].next = s[i+1]
    cups = s[-1].next = s[0]

    def popafter():
        nex = cups.next
        cups.next = nex.next
        return nex
    def move(cups):
        three = [popafter() for _ in range(3)]
        dest_lbl = cups-1
        while dest_lbl in three or not dest_lbl:
            if not dest_lbl: dest_lbl = ma+1
            dest_lbl -= 1
        dest = llmap[dest_lbl]
        aft = dest.next
        dest.next = three[0]
        three[-1].next = aft
        
    for i in range((ma+part1)*10):
        move(cups)
        cups = cups.next
    if not part1: print(llmap[1].next*llmap[1].next.next)
    else: print(''.join(map(str,(v:=llmap[1 if not i else v].next for i in range(ma-1)))))
dowith(9)
dowith(1000000)


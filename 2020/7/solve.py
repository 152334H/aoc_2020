from aoc import *
def parse(l):
    l = l.replace(' bags','').replace(' bag','')
    container, other = l.split(' contain ')
    if 'no other bags.' in other: return container, None
    def proc_item(s):
        num, *desc = s.split()
        if num == 'no': return None
        return ' '.join(desc), int(num)
    return container, dict(filter(lambda t: t is not None, map(proc_item,other.strip('.').split(', '))))
bags = dict(sreadlines('input', parse))
rev_bags = dd(lambda: {})
for n in bags:  # set to 0 to ignore weight
    for c,w in bags[n].items(): rev_bags[c][n] = 0
def BFS(start, d):
    queue, seen = [start], set([start])
    bags = 0
    while queue:
        neq = []
        for bag,weight in queue:
            bags += weight
            for target,w in d[bag].items():
                neq.append(tup := (target,w*weight))
                seen.add(tup)
        queue = neq
    return seen, bags
print(len(BFS(('shiny gold',0), rev_bags)[0])-1)
print(BFS(('shiny gold',1), bags)[1]-1)

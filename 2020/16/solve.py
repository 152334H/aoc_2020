from aoc import *
# parse input
info, ticket, nearby = sread('input', str, '\n\n')
def infoline(l): # note that integer membership query for range() is O(1)
    k, v = l.split(': ')
    t = [Map(int,r.split('-')) for r in v.split(' or ')]
    return (k, tuple(range(r[0], r[1]+1) for r in t))
def ticketline(l): return Map(int,l.split(','))
info = dict(infoline(l) for l in info.split('\n'))
ticket = ticketline(ticket.split('\n')[-1])
nearby = [ticketline(l) for l in nearby.split('\n')[1:]]
# part 1
good_tickets, err = [], 0
for t in nearby:
    errs = [v for v in t if all(v not in r for t in info.values() for r in t)]
    if len(errs): err += sum(errs)
    else: good_tickets.append(t)
print(err)
# part 2
def getvalid(v): return set(k for k in info if any(v in r for r in info[k]))
fields = [set(info.keys()) for _ in range(len(info))]
for t in good_tickets:
    for i,v in enumerate(t): fields[i].intersection_update(getvalid(v))
while not all(len(f) == 1 for f in fields):
    for f in filter(lambda f: len(f)==1, fields):
        [other.__isub__(f) for other in fields if other is not f]
fields = [f.pop() for f in fields]
print(prod(ticket[i] for i,f in enumerate(fields) if 'departure' in f))

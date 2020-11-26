from itertools import combinations as C
with open('input') as f: lines = [list(sorted(map(int,l.strip().split('\t')))) for l in f.read().strip().split('\n')]
print(sum(l[-1]-l[0] for l in lines))
print(sum((lambda t: t[1]//t[0])(next(filter(lambda t: t[1]%t[0] == 0, C(sorted(l),2)))) for l in lines))
from aoc import *
rules, messages = [chunk.split('\n') for chunk in sread('input').split('\n\n')]
def parse_rule(l):
    k, v = l.split(': ')
    k = int(k)
    if '"' in v: return (k,v.replace('"',''))
    possibilities = v.split(' | ')
    return (k,[Map(int,subrule.split(' ')) for subrule in possibilities])
rules = dict(parse_rule(l) for l in rules)

def match(rule, s):
    subrules = rules[rule]
    if isinstance(subrules,str): return (s[0] == subrules, 1)
    # else, is a list of lists
    for subrule in rules[rule]:
        if len(subrule) > len(s): return (False, 0)
        ind = 0
        for r in subrule:
            valid, shift = match(r,s[ind:])
            if not valid: break
            ind += shift
        else: # all were valid
            return (True, ind)
    return (False, 0)
print(sum(valid and size==len(m) for m in messages for valid,size in [match(0,m)]))

rules[8] = [[42], [42,8]]
rules[11] = [[42,31], [42,11,31]]

def match(rule,s):
    subrules = rules[rule]
    if isinstance(subrules,str):
        if s and s[0] == subrules: yield s[1:]
        return
    for subrule in subrules:
        possibilities = [s]   # strings to possibly match
        for r in subrule:
            new_possib = set()
            for p in possibilities:
                for remain in match(r,p): new_possib.add(remain)
            possibilities = new_possib
        yield from possibilities
print(sum(mat=='' for m in messages for mat in match(0,m)))

from aoc import *
from string import hexdigits
def passport_constructor(lines):
    return dict(t.split(':') for t in ' '.join(lines.split('\n')).split(' '))
passports = sread('input', passport_constructor, '\n\n')
KEYS = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
part1, part2 = 0,0
for p in passports:
    if len(KEYS&set(p.keys())) != len(KEYS): continue
    part1 += 1
    # next: part 2 requirements
    if any(
        len(p[k]) != 4 or int(p[k]) not in r for k,r in [
            ('byr', range(1920,2003)),
            ('iyr', range(2010,2021)),
            ('eyr', range(2020,2031))
        ]): continue
    # height requirements will pass in one of the top-level if-statements
    height = int(p['hgt'][:-2])
    if p['hgt'][-2:] == 'cm':
        if height < 150 or height > 193: continue
    elif p['hgt'][-2:] == 'in':
        if height < 59 or height > 76: continue
    else: continue
    # here's everything else.
    if p['hcl'][0] != '#' or len(p['hcl']) != 1+6: continue
    if not all(c in hexdigits for c in p['hcl'][1:]): continue
    if p['ecl'] not in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}: continue
    if len(p['pid']) != 9: continue # the input is always a valid int.
    part2 += 1
print(part1)
print(part2)

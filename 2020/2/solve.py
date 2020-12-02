from aoc import *
s = [(*Map(int,Range.split('-')),char,pw) for policy,pw in sreadlines('input', str, ': ') for Range,char in [policy.split()]]
for cond in [lambda mi,ma,char,pw: mi <= pw.count(char) <= ma,
             lambda mi,ma,char,pw: (pw[mi-1]==char)^(pw[ma-1]==char)]:
    print(sum(map(star(cond), s)))

from aoc import *
from gamecode import *
def parse_instr(l):
    ins, v = l.split()
    return ins, int(v)
loop = sreadlines('input', parse_instr)
# part 1
print(exec_without_repeat(loop)[0])
# part 2
for i,t in enumerate(loop):
    ins, v = t
    if ins == 'acc': continue
    newloop = loop[:]
    newloop[i] = ('nop' if ins == 'jmp' else 'jmp',v)
    accu, RIP = exec_without_repeat(newloop)
    if RIP == len(loop): print(accu)

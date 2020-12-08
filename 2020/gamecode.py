# Expectation: intcode will continue.
def exec_code(loop, cond):
    accu, RIP = 0,0
    seen = set()
    while cond(RIP, accu, seen):
        seen.add(RIP)
        ins, v = loop[RIP] # prediction: this will have more args later on...
        if ins == 'acc': accu += v
        if ins == 'jmp': RIP += v-1
        RIP += 1
    return accu, RIP
def exec_without_repeat(loop):
    return exec_code(loop, lambda RIP,_,seen: RIP not in seen and 0 <= RIP < len(loop))


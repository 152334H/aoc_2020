with open('input') as f: S = f.read().strip()
LEN = len(S)
s = S+S[0]
print(sum(map(lambda v: v//11, filter(lambda v: v%11==0, [int(s[i:i+2]) for i in range(len(s)-1)]))))
print(sum(int(c) for i,c in enumerate(s) if c == s[(i+LEN//2) % LEN]))

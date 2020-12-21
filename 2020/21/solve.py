from aoc import *
def extractor(l):
    ingredients, paren = l.split(' (')
    return set(ingredients.split()), set(paren[len('contains '):-1].split(', '))
s = sreadlines('input', extractor)

# initialising data
all_ingreds,all_allergies = [reduce(lambda a,b:a|b, [t[i] for t in s]) for i in (0,1)]
ingred_count = sum([Counter(t[0]) for t in s],Counter())    # for part 1
allergen_sources = dd(lambda: set(all_ingreds)) # Dict[aller:str, ingreds:set]
for ingred, allergens in s:
    for a in allergens: allergen_sources[a] &= ingred

# determine the dangerous ingreds in allergen_sources[]
while not all(len(v)==1 for v in allergen_sources.values()):
    [sources.difference_update(true_source)
            for a,true_source in allergen_sources.items() if len(true_source) == 1
            for other,sources in allergen_sources.items() if other != a]
for k,s in allergen_sources.items(): allergen_sources[k] = s.pop()

# give out answers for both parts
print(sum(ingred_count[s] for s in all_ingreds-set(allergen_sources.values())))
print(','.join(t[1] for t in sorted(allergen_sources.items())))

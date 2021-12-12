import numpy as np
from functools import reduce
from collections import defaultdict

file = '2020/inputs/d21.txt'


# Read the file
with open(file) as f:
    lines = [line.strip() for line in f if line.strip()]

foods = lines
ingredients = [f.split(' (contains ')[0].split(' ') for f in foods]
allergens = [f.split(' (contains ')[1][:-1].split(', ') for f in foods]

allergens_to_food = defaultdict(list)
for it, (i,a) in enumerate(zip(ingredients, allergens)):
    for aa in a:
        allergens_to_food[aa].append(it)

ingredients_sets = [set(i) for i in ingredients]
allergen_to_possible_ingredients = {}
for a in allergens_to_food:
    allergen_to_possible_ingredients[a] = reduce(lambda x,y: x & y, [ingredients_sets[i] for i in allergens_to_food[a]])
    print(a, list(allergen_to_possible_ingredients[a]))

to_prop = [a for a,v in allergen_to_possible_ingredients.items() if len(v) == 1]
while len(to_prop) > 0:
    a = to_prop.pop()
    v = next(iter(allergen_to_possible_ingredients[a]))
    for b in allergens_to_food:
        pi_b = allergen_to_possible_ingredients[b]
        if b != a and v in pi_b:
            pi_b.remove(v)
            if len(pi_b) == 1:
                to_prop.append(b)

print('allergen_to_possible_ingredients')
for a in allergens_to_food:
    print(a, list(allergen_to_possible_ingredients[a]))

ingredients_with_allergens = set.union(*[allergen_to_possible_ingredients[a] for a in allergens_to_food])
iss = [len(x - ingredients_with_allergens) for x in ingredients_sets]
print('P1', sum(iss))

p2 = ','.join([next(iter(allergen_to_possible_ingredients[a])) for a in sorted(allergens_to_food.keys())])
print('P2', p2)

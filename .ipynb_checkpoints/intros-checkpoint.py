import random

def catch_pikachu(p):
    r = random.random()
    return r<p

#print(sum([catch_pikachu(.2) for _ in range(100)])/100)

print([catch_pikachu(.2) for _ in range(100)])
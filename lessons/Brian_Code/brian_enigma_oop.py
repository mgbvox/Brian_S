import string
import numpy as np
import sys
import json

'''
TODO: Convert to Enigma Class
'''

chars = string.ascii_lowercase

def get_rotor(charset = chars):
    charset = list(charset)
    shuffled = np.random.choice(charset, len(charset), replace=False)
    rotor = dict(zip(charset, shuffled))
    return rotor

def shift(r, n):
    imap = {i:v for i, (k,v) in enumerate(r.items())}
    return {k:imap[(i+n)%len(imap)] for i, (k,v) in enumerate(r.items())}

mode = sys.argv[1]
s = sys.argv[2]

if mode == 'e':
    n_rotors = int(sys.argv[3])
    #Generate char cypher rotors (one-to-one mapping ch1 to ch2)
    rotors = [get_rotor(chars) for _ in range(n_rotors)]
else:
    with open(sys.argv[3]) as json_file:
        rotors = json.load(json_file)
    n_rotors = len(rotors)

#Pre-calculate shifted rotors for each timestep in the encoding process.
shift_sets = {n:[shift(r,n) for r in rotors] for n,c in enumerate(s)}


def forward(c, r_set):
    e = c
    for rotor in r_set:
        e = rotor[e]
    return e


def encode(s):
    print('Encoding...')
    res = ''
    for n, c in enumerate(s):
        r_set = shift_sets[n]
        res += forward(c, r_set)
    return res


def rdict(r):
    return {v:k for k,v in r.items()}


def backward(e, r_set):
    c = e
    for r in r_set[::-1]:
        r = rdict(r) #reverse dict
        c = r[c]
    return c


def decode(es):
    print('Decoding...')
    res = ''
    for n, e in enumerate(es):
        r_set = shift_sets[n]
        res += backward(e, r_set)
    return res


if mode == 'e':
    print(encode(s))
    if not len(sys.argv) == 5:
        mid = np.random.randint(1,1000)
    else:
        mid = sys.argv[4]

    j = json.dumps(rotors)
    f = open(f"{mid}_rotors.json", "w")
    f.write(j)
    f.close()

else:
    print(decode(s))
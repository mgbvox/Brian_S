import string
import numpy as np
import sys
import json

'''
TODO: Convert to Enigma Class
'''
class Enigma:
    def __init__(self, n_rotors):
        self.chars = list(string.ascii_lowercase)
        self.n_rotors = n_rotors
        self.rotors = [self.get_rotor() for _ in range(n_rotors)]


        self.shift_sets = None

    def get_rotor(self):
        shuffled = np.random.choice(self.chars, len(self.chars), replace=False)
        rotor = dict(zip(self.chars, shuffled))
        return rotor

    def shift(self, r, n):
        imap = {i:v for i, (k,v) in enumerate(r.items())}
        return {k:imap[(i+n)%len(imap)] for i, (k,v) in enumerate(r.items())}

    def forward(self, c, r_set):
        e = c
        for rotor in r_set:
            e = rotor[e]
        return e

    def encode(self, s):

        self.shift_sets = {n: [self.shift(r, n) for r in self.rotors] for n, c in enumerate(s)}

        print('Encoding...')
        res = ''
        for n, c in enumerate(s):
            r_set = self.shift_sets[n]
            res += self.forward(c, r_set)
        return res

    def rdict(self, r):
        return {v: k for k, v in r.items()}

    def backward(self, e, r_set):
        c = e
        for r in r_set[::-1]:
            r = self.rdict(r)  # reverse dict
            c = r[c]
        return c

    def decode(self, es):

        self.shift_sets = {n: [self.shift(r, n) for r in self.rotors] for n, c in enumerate(es)}

        print('Decoding...')
        res = ''
        for n, e in enumerate(es):
            r_set = self.shift_sets[n]
            res += self.backward(e, r_set)
        return res

    def save(self, mid):
        j = json.dumps(self.rotors)
        f = open(f"{mid}_rotors.json", "w")
        f.write(j)
        f.close()

    def load(self, rotors_path):
        with open(rotors_path) as json_file:
            self.rotors = json.load(json_file)
        self.n_rotors = len(self.rotors)

import numpy as np
import string
import re
from tqdm import tqdm
import os
from zipfile import ZipFile
import shutil

def zip_dir(path):
    path = path.split('.')[0]
    # create a ZipFile object
    with ZipFile(f'{path}.zip', 'w') as zipObj:
       # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk(f'{path}'):
            for filename in filenames:
               #create complete filepath of file in directory
               filePath = os.path.join(folderName, filename)
               # Add file to zip
               zipObj.write(filePath)

class Enigma:
    def __init__(self, n_rotors = 5, charset = string.printable):
        self.n_rotors = n_rotors
        self.chars = charset

        #Encoding-Specific:
        # Generate char cypher rotors (one-to-one mapping ch1 to ch2)
        self.rotors = [self.gen_rotor(self.chars) for _ in range(self.n_rotors)]
        # PLACEHOLDER (See Encode) -> Pre-calculate shifted rotors for each timestep in the encoding process.
        self.shift_sets = None

    def gen_rotor(self, chars):
        scrambled = np.random.choice(list(chars), len(chars), replace=False)
        return dict(zip(list(chars), scrambled))

    def shift(self, r, n):
        imap = {i:v for i, (k,v) in enumerate(r.items())}
        return {k:imap[(i+n)%len(imap)] for i, (k,v) in enumerate(r.items())}

    def forward(self, c, r_set):
        e_hist = []
        e = c
        for r in r_set:
            e_hist.append(e)
            e = r[e]
        return e

    def rdict(self, d):
        return {v:k for k,v in d.items()}

    def backward(self, e, r_set):
        c_hist = []
        c = e
        for r in r_set[::-1]:
            r = self.rdict(r) #reverse dict
            c_hist.append(c)
            c = r[c]
        return c

    def encode(self, s = 'Placeholder', from_path = False, path = None):
        if from_path:
            s = self.read_text(path)
        elif s == 'Placeholder':
            raise ValueError('Please pass a string to encode.')

        # Pre-calculate shifted rotors for each timestep in the encoding process.
        self.shift_sets = {n: [self.shift(r, n) for r in self.rotors] for n, c in enumerate(s)}

        res = ''
        for n, c in enumerate(s):
            r_set = self.shift_sets[n]
            res += self.forward(c, r_set)
        return res

    def decode(self, es):
        # Pre-calculate shifted rotors for each timestep in the encoding process.
        self.shift_sets = {n: [self.shift(r, n) for r in self.rotors] for n, e in enumerate(es)}

        print('Decoding...')
        res = ''
        for n, e in enumerate(es):
            r_set = self.shift_sets[n]
            res += self.backward(e, r_set)
        return res

    def read_text(self, path):
        with open(path, 'r') as f:
            text = ' '.join([l.strip() for l in f.readlines()])
            text = re.sub(f'[^{self.chars}]', '', text)
            return text

    def save(self, name):
        root = f'{name}_Enigma_Settings'
        rotor_path = os.path.join(root, 'rotors')
        char_path = os.path.join(root, 'charset')

        if not os.path.exists(root):
            os.mkdir(root)
            os.mkdir(rotor_path)
            os.mkdir(char_path)

        np.save(os.path.join(rotor_path, name+'_rotors'), self.rotors)
        np.save(os.path.join(char_path, name+'_charset'), self.chars)

        zip_dir(root)
        shutil.rmtree(root)


    #def load(self, path):




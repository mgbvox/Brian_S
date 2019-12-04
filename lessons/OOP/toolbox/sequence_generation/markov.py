import pandas as pd
import numpy as np
from tqdm import tqdm


class MarkovSeqGen:
    def __init__(self, seqs, start='>', stop='|'):
        self.seqs = pd.Series(seqs)
        self.start = start
        self.stop = stop
        self.seqs = self.seqs.apply(lambda x: self.start + x + self.stop)
        self.chars = sorted(set(''.join(self.seqs)))

        self.c_to_i = {c: i for i, c in enumerate(self.chars)}
        self.i_to_c = {v: k for k, v in self.c_to_i.items()}

        self.tmat = self.encode_tmat()

    def encode_tmat(self):
        tmat = np.zeros((len(self.chars), len(self.chars)))
        for n, seq in tqdm(enumerate(self.seqs)):
            for cidx, c in enumerate(seq):
                if cidx > 0:
                    a = seq[cidx - 1]
                    b = seq[cidx]
                    i = self.c_to_i[a]
                    j = self.c_to_i[b]
                    tmat[i, j] += 1
        return tmat

    def gen(self, n):
        seqs = []
        for _ in range(n):
            res = ''
            res += self.start
            curr = res[-1]
            while curr != self.stop:
                cur_i = self.c_to_i[curr]
                probs = self.tmat[cur_i] / self.tmat[cur_i].sum()
                res += np.random.choice(self.chars, p=probs)
                curr = res[-1]
            seqs.append(res[1:-1])
        return seqs
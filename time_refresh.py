#!/usr/bin/env python3

import pickle
import os
from payout import Payout, reorderUsers 

path = os.path.dirname(os.path.realpath(__file__)) + '/data.pkl'
print(path)

with open(path, 'rb') as input:
    payList = pickle.load(input)

def refresh():
    for p in payList:
        reorderUsers(p)
    with open(path, 'wb') as output:
            pickle.dump(payList, output)

refresh()

#!/usr/bin/env python3

import pickle
import os
from payout import Payout, reorderUsers 
#os.chdir('/home/kyle/Documents/rank-bot')
path = os.getcwd() + '/data.pkl'

with open('/home/kyle/Documents/discord/rank-bot/data.pkl', 'rb') as input:
    payList = pickle.load(input)

def refresh():
    for p in payList:
        reorderUsers(p)
    with open('/home/kyle/Documents/discord/rank-bot/data.pkl', 'wb') as output:
            pickle.dump(payList, output)

refresh()

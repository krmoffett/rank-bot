#!/usr/bin/env python3

import pickle
from payout import *

payList = []

pay1 = Payout("1:00")
pay1.users = ["Tommy Bombadil", "Chowbacca", "Oromis"]
payList.append(pay1)

# Write to file
with open('data.pkl', 'wb') as output:
    pickle.dump(payList, output, pickle.HIGHEST_PROTOCOL)

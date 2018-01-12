#!/usr/bin/env python3

import pickle
from payout import *

payList = []

pay1 = Payout(1, 0)
pay1.users = ["Tommy Bombadil", "Chowbacca", "Oromis"]
payList.append(pay1)

pay2 = Payout(2, 0)
pay2.users = ["Darcdath", "hurricain", "Ftalten 66"]
payList.append(pay2)

pay9 = Payout(9, 0)
pay9.users = ["C3P SHIRO"]
payList.append(pay9)

pay0 = Payout(0, 0)
pay0.users = ["Knil", "Rhaegar"]
payList.append(pay0)

pay1230 = Payout(12, 30)
pay1230.users = ["Yeheya"]
payList.append(pay1230)

pay15 = Payout(15, 0)
pay15.users = ["Kanier"]
payList.append(pay15)

pay17 = Payout(17, 0)
pay17.users = ["Snatsh", "Curio", "Thoby", "Six", "QBA", "Error"]
payList.append(pay17)

pay18 = Payout(18, 0)
pay18.users = ["Eckle", "Roykenneth", "Sisyphus"]
payList.append(pay18)

pay21 = Payout(21, 0)
pay21.users = ["jediloco"]
payList.append(pay21)

pay23 = Payout(23, 0)
pay23.users = ["Shrike", "Darthpool", "Howler24", "Shuglin"]
payList.append(pay23)

# Write to file
with open('data.pkl', 'wb+') as output:
    pickle.dump(payList, output)

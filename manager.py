#!/usr/bin/env python3

import pickle
from payout import *

payList = []

pay1 = Payout("01:00")
pay1.users = ["Tommy Bombadil", "Chowbacca", "Oromis"]
payList.append(pay1)

pay2 = Payout("02:00")
pay2.users = ["Darcdath", "hurricain", "Ftalten 66"]
payList.append(pay2)

pay9 = Payout("09:00")
pay9.users = ["C3P SHIRO"]
payList.append(pay9)

pay0 = Payout("00:00")
pay0.users = ["Knil", "Rhaegar"]
payList.append(pay0)

pay1230 = Payout("12:30")
pay1230.users = ["Yeheya"]
payList.append(pay1230)

pay15 = Payout("15:00")
pay15.users = ["Kanier"]
payList.append(pay15)

pay17 = Payout("17:00")
pay17.users = ["Snatsh", "Curio", "Thoby", "Tharos", "Six", "Error"]
payList.append(pay17)

pay18 = Payout("18:00")
pay18.users = ["Eckle", "Roykenneth", "Sisyphus"]
payList.append(pay18)

pay21 = Payout("21:00")
pay21.users = ["jediloco"]
payList.append(pay21)

pay23 = Payout("23:00")
pay23.users = ["Shrike", "Vintage Lawyer", "Shuglim", "Howler24"]
payList.append(pay23)

# Write to file
with open('data.pkl', 'wb') as output:
    pickle.dump(payList, output, pickle.HIGHEST_PROTOCOL)

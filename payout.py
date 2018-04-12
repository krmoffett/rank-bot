from datetime import datetime, MINYEAR 

class Payout():
    def __init__(self, hour, minute):
        self.payTime = datetime(MINYEAR, 1, 1, hour, minute, 0, 0)
        self.users = []
        
    def printTimeUntil(self):
        currentDay = datetime.now()
        diff = self.payTime - currentDay
        hours = divmod(diff.seconds, 3600)
        minutes = divmod(hours[1], 60)
        
        return (str(hours[0]) + ":" + "{0:0=2d}".format(minutes[0]))

    def getTimeUntil(self):
        currentDay = datetime.now()
        diff = self.payTime - currentDay
        hours = divmod(diff.seconds, 3600)
        minutes = divmod(hours[1], 60)

        return (hours, minutes)

    def getHoursUntil(self):
        currentDay = datetime.now()
        diff = self.payTime - currentDay
        hours = divmod(diff.seconds, 3600)
        return hours[0]  

    def setAtIndex(self, player, index):
        currentIndex = 0
        for idx,u in enumerate(self.users):
            if player.lower() in u.lower():
                currentIndex = idx
                break
        self.users.pop(currentIndex)
        self.users.insert(index - 1, player)
                

def printPayout(myPay):
    returnText = []
    for i,u in enumerate(myPay.users):
        returnText.append("" + str(i + 1) + ". " + u)
    return returnText

def reorderUsers(myPay):
    first = myPay.users.pop(0)
    myPay.users.append(first)

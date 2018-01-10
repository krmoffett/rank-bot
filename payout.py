from datetime import *

class Payout(object):
	def __init__(self, hour, minute):
		self.payTime = time(hour, minute)
        
        def printTimeUntil(self):
            currentTime = datetime.now()
            d_hours = self.payTime.hour - currentTime.hour
            d_minutes = self.payTime.minute - currentTime.minute + 60
            return ("Time until payout: " + str(d_hours) + ":" + str(delta_minutes))

	users = []

def printPayout(myPay):
    returnText = []
    for i,u in enumerate(myPay.users):
        returnText.append("\t" + str(i + 1) + ". " + u)
    return returnText

def reorderUsers(myPay):
    first = myPay.users.pop(0)
    myPay.users.append(first)

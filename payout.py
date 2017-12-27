class Payout(object):
	def __init__(self, time):
		self.time = time
	users = []

def printPayout(myPay):
    returnText = []
    for i,u in enumerate(myPay.users):
        returnText.append(str(i + 1) + ". " + u)
    return returnText

def reorderUsers(myPay):
    first = myPay.users.pop(0)
    myPay.users.append(first)

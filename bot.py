#!/usr/bin/env python3
import discord
import asyncio
import datetime
import json
import pickle
import sys
from payout import * 

client = discord.Client()

now = datetime.datetime.now()
currentDay = now.day
#currentDay = 26

# Read data file
with open('data.pkl', 'rb') as input:
    payList = pickle.load(input)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
# Receive message
async def on_message(message):
    now = datetime.datetime.now()   # Update day and reorder payout time if new day
    if now.day != currentDay:
        for p in payList:
            reorderUsers(p)
        with open('test.pkl', 'wb') as output:
            pickle.dump(payList, output, pickle.HIGHEST_PROTOCOL)
        global currentDay
        currentDay = now.day

    usrIn = message.content.split()

    if message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
	
    elif usrIn[0] == '!payout':
        text = []
        time = ""
        usrFound = 0
#        if len(usrIn) == 1:
#            text = printPayout(myPayout)
#            time = myPayout.time
#            usrFound = 1
        if len(usrIn) >= 2:
            user = ""
            for idx,val in enumerate(usrIn[1:]):
                if idx == 0:
                    user = val
                else:
                    user = user + " "  + val
            for p in payList:
                for u in p.users:
                    if user.lower() in u.lower():
                        text = printPayout(p)
                        time = p.time
                        usrFound = 1
                        break
        if usrFound == 1:
            output = "The schedule for todays payout at " + str(time) + " UTC is:"
            await client.send_message(message.channel, output)
#            for t in text:
#                await client.send_message(message.channel, t)
            sendtxt = ""
            for idx, t in enumerate(text):
                if idx == 0:
                    sendtxt = text[idx]
                else:
                    sendtxt = sendtxt + "\n" + text[idx]
            await client.send_message(message.channel, sendtxt)
            
        else:
            await client.send_message(message.channel, "Username not found")

    elif usrIn[0] == '!hello':
        print ("Hello there")

    elif usrIn[0] == '$shutdown':
        with open('test.pkl', 'wb') as output:
            pickle.dump(payList, output, pickle.HIGHEST_PROTOCOL)
        sys.exit()

    elif usrIn[0] == '$reorder':
        for p in payList:
            reorderUsers(p)
        with open('test.pkl', 'wb') as output:
            pickle.dump(payList, output, pickle.HIGHEST_PROTOCOL)

    elif usrIn[0] == '!help':
        output = "Use !payout <username> to see the rank and time for specified user"
        await client.send_message(message.channel, output)

#    else:
#        output = "Command \"" + message.content + "\" not valid." 
#        await client.send_message(message.channel, output)
        

client.run('Mzk1NDI4NzEwNzQxNzA0NzA0.DSgULw.zcFH-j8TVQk5rnCY-ALlFHkHDy0')


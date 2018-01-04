#!/usr/bin/env python3
import discord
import asyncio
from datetime import datetime
import json
import pickle
import sys
from threading import Timer
from payout import * 

client = discord.Client()

# Set up timer for daily refresh
x = datetime.today()
y = x.replace(day=x.day+1, hour = 2, minute=0, second=0, microsecond=0)
delta_t = y - x
secs = delta_t.seconds + 1

def refresh():
    for p in payList:
        reorderUsers(p)
    with open('data.pkl', 'wb') as output:
            pickle.dump(payList, output)

t = Timer(secs, refresh)
t.start()

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

    usrIn = message.content.split()

    if usrIn[0] == '!payout':
        text = []
        time = ""
        usrFound = 0
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
            output = "The order for today's payout at " + str(time) + " UTC is:"
            sendtxt = ""
            for idx, t in enumerate(text):
                if idx == 0:
                    sendtxt = text[idx]
                else:
                    sendtxt = sendtxt + "\n" + text[idx]
            output = output + "\n\n" + sendtxt
            await client.send_message(message.channel, output)
            
        else:
            await client.send_message(message.channel, "Username not found")

    elif usrIn[0] == '!hello':
        print ("Hello there")

    elif usrIn[0] == '$shutdown':   #exit bot while saving data
        with open('data.pkl', 'wb') as output:
            pickle.dump(payList, output)
        sys.exit()
    
    elif usrIn[0] == '$write':  #save payouts to file
        with open('data.pkl', 'wb') as output:
            pickle.dump(payList, output)

    elif usrIn[0] == '$reorder':    #reorder avery payout by one
        for p in payList:
            reorderUsers(p)
        with open('data.pkl', 'wb') as output:
            pickle.dump(payList, output)

    elif usrIn[0] == '$setFirst':   #$setFirst <username>
        if len(usrIn) < 2:
            output = "Please give name of user to set as 1."
            await client.send_message(message.channel, output)
        elif len(usrIn) >= 2:
            user = ""
            time = ""
            output = ""
            index = 0;
            for idx,val in enumerate(usrIn[1:]):
                if idx == 0:
                    user = val
                else:
                    user = user + " "  + val
            print ("Setting first: " + user)
            for idx,p in enumerate(payList):
                for u in p.users:
                    if user.lower() in u.lower():
                        index = idx 
                        break
            print ("reordering" + payList[index].users[0])
            while (payList[index].users[0] != user):
                reorderUsers(payList[index])
            with open('data.pkl', 'wb') as output:
                pickle.dump(payList, output)

            print ("Done")
            output = "Ranks for payout " + time + " reodered for rank 1:" + user
            await client.send_message(message.channel, output)

    elif usrIn[0] == '!help':
        output = "Use !payout <username> to see the rank and time for specified user"
        await client.send_message(message.channel, output)

# Live bot token
client.run('Mzk1NDI4NzEwNzQxNzA0NzA0.DS2bqw.wIQdvEoYSi-SCGVIIUOSZ6zSb48')

# Test bot token
#client.run('Mzk2MzU0NTgxMDYxMTczMjYx.DS6MhA.hsCDim-0RHcfFpb-O4fmNFfC8EE')

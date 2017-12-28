#!/usr/bin/env python3
import discord
import asyncio
import datetime
import json
import pickle
from payout import * 

client = discord.Client()

now = datetime.datetime.now()
currentDay = now.day
#currentDay = 26
#payList = []

#output_json = json.load(open("dat.json"))
#print (output_json)
#myPayout = Payout("1:00")
#myPayout.users = ["Tommy Bombadil", "Chewbacca", "Oromis"]
#payList.append(myPayout)
#
#with open("payouts.pkl", 'wb') as output:
#    pickle.dump(myPayout, output, pickle.HIGHEST_PROTOCOL)
#
#del myPayout

with open('data.pkl', 'rb') as input:
    payList = pickle.load(input)
#payList.append(pay1)
#with open("dat.json", 'w') as f:
#    json.dump(myPayout.__dict__, f)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    now = datetime.datetime.now()
    if now.day != currentDay:
        for p in payList:
            reorderUsers(p)
        with open('data.pkl', 'wb') as output:
            pickle.dump(payList, output, pickle.HIGHEST_PROTOCOL)

    usrIn = message.content.split()
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
	
    elif usrIn[0] == '!payout':
        text = []
        time = ""
        usrFound = 0
        if len(usrIn) == 1:
            text = printPayout(myPayout)
            time = myPayout.time
            usrFound = 1
        elif len(usrIn) >= 2:
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
            for t in text:
                await client.send_message(message.channel, t)

        else:
            await client.send_message(message.channel, "Username not found")

    elif usrIn[0] == '!hello':
        print ("Hello there")

client.run('Mzk1NDI4NzEwNzQxNzA0NzA0.DSVqng.BmVzSR_jgqplCsn4sxvZuBGQq5g')


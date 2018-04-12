#!/usr/bin/env python3
from discord.ext import commands
import discord
import asyncio
import collections
from datetime import * 
import pickle
import sys
from threading import Timer
from payout import * 
from auth import *
import configparser
import os.path

config = configparser.ConfigParser()
config.read('config.ini')
defaultConfig = config['DEFAULT']
token = defaultConfig['bot_token']
prefix = defaultConfig['prefix']

bot = commands.Bot(command_prefix=prefix)

def readPayoutFile():
    if not os.path.isfile('data.pkl'):
        with open('data.pkl', 'w+') as input:
            pass
    with open('data.pkl', 'rb') as input:
        payList = pickle.load(input)
        return payList

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(pass_context=True)
async def payout(ctx, user : str):
    """Prints the payout rankings of the specified user

    Parameters:
    user -- the user to get the payout for
    """
    payList = readPayoutFile()
    print ("command payout")
    userFound = False
    em = discord.Embed(colour=0x55B5FF)
    output = "new"
    for p in payList:
        for u in p.users:
            if user.lower() in u.lower():
                text = printPayout(p)
                time = p.payTime
                timeUntil = p.printTimeUntil()
                userFound = True
                break
    if userFound == True:
        em.title = "The order for today's payout at " + str(time.hour) + ":" + "{0:0=2d}".format(time.minute) + " UTC is:"
        sendtxt = ""
        for idx, t in enumerate(text):
            if idx == 0:
                sendtxt = text[idx]
            else:
                sendtxt = sendtxt + "\n" + text[idx]
        output = output + "\n\n" + sendtxt + "\n\nTime until payout:` " + timeUntil + "`"
        em.description = output
        await bot.send_message(ctx.message.channel, embed=em)
        
    else:
        await bot.say("Username not found")
     
@bot.command(pass_context=True)
async def payouts(ctx):
    """Prints a list of all payouts with the time left before each"""
    payList = readPayoutFile()
    em = discord.Embed(title='Time left before next payout:', colour=0x55B5FF)
    output = ""
    payout_dict = {}
    for p in payList:
        key = p.getHoursUntil()
        payout_dict[key] = p
    od_payout_dict = collections.OrderedDict(sorted(payout_dict.items()))
    for key in od_payout_dict:
        output += "**" + od_payout_dict[key].printTimeUntil() + "** - "
        for idx,u in enumerate(od_payout_dict[key].users):
            output += u
            if idx != len(od_payout_dict[key].users) - 1:
                output += " - "
        output += "\n"
    em.description = output
    await bot.send_message(ctx.message.channel, embed=em)

@bot.command(pass_context=True)
async def avoid(ctx):
    """Prints a list of players with payouts within 4 hours"""
    payList = readPayoutFile()
    em = discord.Embed(title="The following have upcoming payouts. Please avoid attacking them:", colour=0x55B5FF)
    sendtxt = ""
    usersToAvoid = [] 
    for p in payList:
        if p.getHoursUntil() <= 4:
            for u in p.users:
                usersToAvoid.append(u)
    userToAvoid = usersToAvoid.sort(key=str.lower)
    for i,u in enumerate(usersToAvoid):
        if i == len(usersToAvoid) - 1:
            sendtxt += u
        else:
            sendtxt += u + ', '

        if len(usersToAvoid) == 0:
            sendtxt = "No one has an upcoming payout"
        em.description = sendtxt
    await bot.send_message(ctx.message.channel, embed=em)

@bot.command(pass_context=True)
async def set(ctx, position: int, player : str):
    """Sets the given player to the given rank in their payout
    NOT CURRENTLY WORKING
    Parameters:
    position -- the desired position of the player
    player -- the name of the player to set to first
    """
    payList = readPayoutFile()
    index = 0
    time = ""
    payoutIndex = 0

    playerFound = False
    for idx,p in enumerate(payList):
        for u in p.users:
            if player.lower() in u.lower():
                index = idx 
                playerFound = True
                time = p.payTime
                payoutIndex = idx
                break
    if playerFound == True:
#        found_player = payList[payoutIndex].users.pop(index)
#        payList[payoutIndex].users.insert(position, found_player)
#        with open('data.pkl', 'wb') as output:
#            pickle.dump(payList, output)

        output = "Ranks for payout " + str(time.hour) + ":" + "{0:0=2d}".format(time.minute) + " changed"
        await bot.say(output)
    else:
        bot.say("Player name not found")

""" @bot.event
# Receive message
async def on_message(message):
    if len(message.content) > 0:
        if message.content[0] == '!' or message.content[0] == '$':
            print(message.author)
            print(message.content)
            # Read data file
#            with open('data.pkl', 'rb') as input:
 #               payList = pickle.load(input)
    payList = [] 
    usrIn = []
    usrIn = message.content.split()
    if len(usrIn) < 2:
        usrIn.append('blank')

#    if usrIn[0] == '!payout':
#        text = []
#        time = ""
#        em = discord.Embed(colour=0x55B5FF)
#        timeUntil = ""
#        usrFound = 0
#        output = ""
#        if len(usrIn) >= 2:
#            user = ""
#            for idx,val in enumerate(usrIn[1:]):
#                if idx == 0:
#                    user = val
#                else:
#                    user = user + " "  + val
#            for p in payList:
#                for u in p.users:
#                    if user.lower() in u.lower():
#                        text = printPayout(p)
#                        time = p.payTime
#                        timeUntil = p.printTimeUntil()
#                        usrFound = 1
#                        break
#        if usrFound == 1:
#            em.title = "The order for today's payout at " + str(time.hour) + ":" + "{0:0=2d}".format(time.minute) + " UTC is:"
#            sendtxt = ""
#            for idx, t in enumerate(text):
#                if idx == 0:
#                    sendtxt = text[idx]
#                else:
#                    sendtxt = sendtxt + "\n" + text[idx]
#            output = output + "\n\n" + sendtxt + "\n\nTime until payout:` " + timeUntil + "`"
##            output = "```" + output + "```"
#            em.description = output
#            await bot.send_message(message.channel, embed=em)
#            
#        else:
#            await bot.send_message(message.channel, "```Username not found```")

    elif usrIn[0] == '!payouts':
        em = discord.Embed(title='Time left before next payout:', colour=0x55B5FF)
        output = ""
        payout_dict = {}
        for p in payList:
            key = p.getHoursUntil()
            payout_dict[key] = p
        od_payout_dict = collections.OrderedDict(sorted(payout_dict.items()))
#        for key in od_payout_dict:
#            print (key, od_payout_dict[key].users)
        for key in od_payout_dict:
            output += "**" + od_payout_dict[key].printTimeUntil() + "** - "
            for idx,u in enumerate(od_payout_dict[key].users):
                output += u
                if idx != len(od_payout_dict[key].users) - 1:
                    output += " - "
            output += "\n"
        em.description = output
        await bot.send_message(message.channel, embed=em)

    elif usrIn[0] == '!avoid':
        em = discord.Embed(title="The following have upcoming payouts. Please avoid attacking them:", colour=0x55B5FF)
        sendtxt = ""
        usersToAvoid = []
        for p in payList:
            if p.getHoursUntil() <= 4:
                usersToAvoid += p.users
        userToAvoid = usersToAvoid.sort(key=str.lower)
        for i,u in enumerate(usersToAvoid):
            if i == len(usersToAvoid) - 1:
                sendtxt += u
            else:
                sendtxt += u + ', '

#        sendtxt = "```" + sendtxt + "```"
        if len(usersToAvoid) == 0:
            sendtxt = "No one has an upcoming payout"
        em.description = sendtxt
        await bot.send_message(message.channel, embed=em)

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
            await bot.send_message(message.channel, output)
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
            await bot.send_message(message.channel, output)

    elif usrIn[0] == '!help':
        output = "Use !payout <username> to see the rank and time for specified user"
        output = "```" + output + "```"
        await bot.send_message(message.channel, output)

    elif usrIn[0] == '$addUser':
        newTime = usrIn[1]
        newHour = newTime.split(':')[0]
        newMinute = newTime.split(':')[1]
        user = ""
        sendtxt = ""
        for idx,val in enumerate(usrIn[2:]):
            if idx == 0:
                user = val
            else:
                user = user + " "  + val
        print ("Adding " + user)
        timeFound = 0
        index = 0
        for idx,p in enumerate(payList):
            if p.payTime.hour == int(newHour) and p.payTime.minute == int(newMinute):
                timeFound = 1
                index = idx
                break
        if timeFound == 1:
            payList[index].users.append(user)
        else:
            newPayout = Payout(newHour, newMinute)
            newPayout.users = [user]
            payList.append(newPayout)

        with open('data.pkl', 'wb') as output:
            pickle.dump(payList, output)

        sendtxt = "Added " + user + " to payout at " + newTime
        await bot.send_message(message.channel, sendtxt)

    elif usrIn[0] == '$delUser':
        user = ""
        sendtxt = ""
        for idx,val in enumerate(usrIn[1:]):
            if idx == 0:
                user = val
            else:
                user = user + " "  + val

        for p in payList:
            for u in p.users:
                if user.lower() in u.lower():
                    p.users.remove(u)
                    sendtxt = "Removed " + u
                    await bot.send_message(message.channel, sendtxt)
                    break
    
        with open('data.pkl', 'wb') as output:
            pickle.dump(payList, output) """

if __name__ == "__main__":
    bot.run(token)
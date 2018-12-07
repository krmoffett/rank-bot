#!/usr/bin/env python3
from discord.ext import commands
from datetime import datetime 
from payout import Payout, printPayout, reorderUsers 
import discord
import asyncio
import collections
import pickle
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

@bot.event
# Receive message
async def on_message(message):
    if len(message.content) > 0:
        if message.content.startswith(prefix):
            print(message.author)
            print(message.content)
    await bot.process_commands(message)

@bot.command(pass_context=True)
async def payout(ctx, user : str):
    """Prints the payout rankings of the specified user

    Parameters:
    user -- the user to get the payout for
    """
    payList = readPayoutFile()
    userFound = False
    em = discord.Embed(colour=0x55B5FF)
    output = ""
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
    usersToAvoid = usersToAvoid.sort(key=str.lower)
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

    Parameters:
    position -- the desired position of the player
    player -- the name of the player to set to first
    """
    payList = readPayoutFile()
    for p in payList:
        found = False
        for u in p.users:
            if player.lower() in u.lower():
                found = True
        if found == True:
            p.setAtIndex(player, position)
            with open('data.pkl', 'wb') as output:
                pickle.dump(payList, output)
            await bot.say("Payout updated")
            return    

    output = "Ranks for payout changed"
    await bot.say(output)

@bot.command()
async def add(time : str, player : str):
    """Adds the given player at the given time

    Parameters:
    time -- the time for payout given as HH:MM
    player -- the name of the player to add (no spaces)
    """
    payList = readPayoutFile()
    newTime = time
    newHour = newTime.split(':')[0]
    newMinute = newTime.split(':')[1]
    sendtxt = ""
    
    print ("Adding " + player)
    timeFound = 0
    index = 0
    for idx,p in enumerate(payList):
        if p.payTime.hour == int(newHour) and p.payTime.minute == int(newMinute):
            timeFound = 1
            index = idx
            break
    if timeFound == 1:
        payList[index].users.append(player)
    else:
        newPayout = Payout(int(newHour), int(newMinute))
        newPayout.users = [player]
        payList.append(newPayout)

    with open('data.pkl', 'wb') as output:
        pickle.dump(payList, output)

    sendtxt = "Added " + player + " to payout at " + newTime
    await bot.say(sendtxt)

@bot.command()
async def remove(*, player : str):
    """Removes the specified user from payouts
    
    Parameters:
    player -- the name of the player to be removed
    """
    payList = readPayoutFile()
    sendtxt = ""

    for p in payList:
        for u in p.users:
            if player.lower() == u.lower():
                p.users.remove(u)
                sendtxt = "Removed " + u
                if len(p.users) == 0:
                    payList.remove(p)
                with open('data.pkl', 'wb') as output:
                    pickle.dump(payList, output)
                await bot.say(sendtxt)
                return

  #  with open('data.pkl', 'wb') as output:
  #      pickle.dump(payList, output)

@bot.command()
async def rename(current_name : str, new_name : str):
    """Allows player to change the name on the bot

    Parameters:
    current_name -- current player name
    new_name -- desired new name
    """
    await bot.say("Attempting to change name")
    payList = readPayoutFile()
    found = False

    for p in payList:
        for u in p.users:
            if current_name.lower() in u.lower():
                p.rename(current_name, new_name)
                await bot.say("Username changed to " + new_name)
                found = True
                with open('data.pkl', 'wb') as output:
                    pickle.dump(payList, output)
                break
    if not found:
        await bot.say("Could not change name")

@bot.command()
async def rotate(time : str):
    """Rotates the specified payout through one day

    Parameters:
    player_name -- the name of a player in the desired payout
    time -- the payout time of the desired payout
    """
    payList = readPayoutFile()
    hour = time.split(':')[0]
    minute = time.split(':')[1]
    for p in payList:
        if p.payTime.hour == int(hour) and p.payTime.minute == int(minute):
            reorderUsers(p)
            with open('data.pkl', 'wb') as output:
                pickle.dump(payList, output)
            await bot.say("Rotated payout at {}:{}".format(hour, minute))
            return
    await bot.say("Could not rotate payout")

if __name__ == "__main__":
    bot.run(token)
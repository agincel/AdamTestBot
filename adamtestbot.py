import requests
import time
import sys
import datetime
import csv
import random
import re
import json
import traceback
import os
import telegram
import gc
import signal
from threading import Thread

import builtins #I'm so sorry
from pydblite import Base #The PyDbLite stuff

import src.atbCommands as atbCommands
import src.atbFirebase as atbFirebase
from src.atbCommands import atbBlaze

APIKEY = ''
with open('../apikey.csv', 'r+') as csvfile: #apikey is not stored on git, sorry
    reader = csv.DictReader(csvfile)
    APIKEY = list(reader)[0]['key']

atb = telegram.Bot(token=APIKEY)

updates = {}
currentMessage = {}

print("@AdamTestBot 3.95 - Ready to go!")
print("Written by Adam Gincel, rewritten by Matt Gomez, shoutouts to Smesh, SG(DC)^2, and Meth Jelly.")

newestOffset = 0
networkFailure = True
while networkFailure:
    try:
        updates = atb.getUpdates(offset=newestOffset, timeout=3, network_delay=5)
        for u in updates:
            newestOffset = u.update_id
        networkFailure = False
    except Exception:
        print(traceback.format_exc())
        print("...", end=' ')
print("...Connected!")

startTime = datetime.datetime.now()

previousTime = datetime.datetime.now().time()
currentTime = 0

instanceAge = 0
user_id = 0
delayTime = .15

# persistent blaze information

builtins.blazeDB = Base('chatStorage/blaze.pdl') #The path to the database
builtins.blazeDB.create('id', 'name', 'score', 'AMtimestamp', 'PMtimestamp', 'streak', 'penalty', 'topThree', mode="open") #Create a new DB if one doesn't exist. If it does, open it

builtins.blazeList = list()
builtins.groupsBlazed = list()
builtins.blazeMessage = ""

builtins.btcDB = Base('chatStorage/btc.pdl') #the path to the btc database
builtins.btcDB.create('id', 'username', 'name', 'money', 'myYield', 'positiveMultiplier', 'positiveYields', 'zeroMultiplier', 'zeroYields', 'negativeMultiplier', 'negativeYields', 'chat_id', 'stocks', 'other', mode="open")

builtins.btcStockDB = Base('chatStorage/btcStock.pdl')
builtins.btcStockDB.create('name', 'description', 'letter', 'fullRange', 'subRangeSize', 'selectedSubRangeStart', 'currentValue', 'history', 'forecast', mode="open")

builtins.btcDB1 = Base('chatStorage/btc1.pdl')
builtins.btcDB1.create('id', 'username', 'name', 'money', 'myYield', 'positiveMultiplier', 'positiveYields', 'zeroMultiplier', 'zeroYields', 'negativeMultiplier', 'negativeYields', 'chat_id', 'stocks', 'other', mode="open")
# END persistent blaze information

builtins.markov = None
builtins.markovText = ""

blacklist = [-23535579, -28477145]

running = True
while running:
    networkFailure = True
    while networkFailure:
        try:
            updates = atb.getUpdates(offset=newestOffset + 1)
            for u in updates:
                newestOffset = u.update_id
            networkFailure = False
        except Exception:
            print("...")

    if instanceAge % 10 == 0: #print 1 X every ten ticks
        print("Y")
    else:
        print("X", end=" ")

    for u in updates:
        currentMessage = u.message
        try:
            user_id = currentMessage.chat.id
            if user_id not in blacklist:
                parsedCommand = re.split(r'[@\s:,\'*]', currentMessage.text.lower())[0]
                atbCommands.process(atb, user_id, parsedCommand, currentMessage.text, currentMessage, u, datetime.datetime.now() - startTime)

        except Exception as myException:
            try:
                print(traceback.format_exc())
            except:
                print("Welp, something went wrong...")

    currentTime = datetime.datetime.now().time()
    if previousTime.minute != currentTime.minute: # a minute has passed
        if currentTime.hour == 16 and currentTime.minute == 19: #reset for PM blaze
            K = list()
            for user in builtins.blazeDB:
                builtins.blazeDB.update(user, topThree=False)
            builtins.blazeDB.commit()
            builtins.blazeList = list()
            builtins.groupsBlazed = list()
        if (currentTime.hour == 16 and currentTime.minute == 21) or (currentTime.hour == 4 and currentTime.minute == 21): #commit Blaze Database
            builtins.blazeDB.commit()
            atb.sendDocument(chat_id=-12788453, document=open("chatStorage/blaze.pdl", "rb"))
            if currentTime.hour == 16 and currentTime.minute == 21:
                s = set(builtins.groupsBlazed)
                builtins.groupsBlazed = list(s)
                for group in builtins.groupsBlazed:
                    atb.sendMessage(int(group), atbBlaze.blazesummary(datetime.datetime.now()))

        #calculate BTC once per hour
        if currentTime.minute == 0: #it's the start of an hour
            for user in builtins.btcDB:
                if user['username'] == 'Dark_Shadowfall': #legacy, just do it for Mahoney
                    builtins.btcDB.update(user, money=int(user['money'] + user['myYield']))
            buitlins.btcDB.commit()

        if (currentTime.minute % 5) == 0: #every five minutes update the firebase
            try:
                atbFirebase.update()
            except:
                print(traceback.format_exc())

    previousTime = currentTime
    gc.collect()
    instanceAge += 1
    time.sleep(delayTime)

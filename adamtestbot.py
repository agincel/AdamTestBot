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

import src.atbCommands as atbCommands

APIKEY = ''
with open('../apikey.csv', 'r+') as csvfile: #apikey is not stored on git, sorry
    reader = csv.DictReader(csvfile)
    APIKEY = list(reader)[0]['key']

atb = telegram.Bot(token=APIKEY)

updates = {}
currentMessage = {}

print "@AdamTestBot 2.0 - Ready to go!"
print "Written by Adam Gincel, shoutouts to Smesh and KARMA"

newestOffset = 0
networkFailure = True
while networkFailure:
    try:
        updates = atb.getUpdates(offset=newestOffset)
        for u in updates:
            newestOffset = u.update_id
        networkFailure = False
    except Exception:
        print traceback.format_exc()
        print "...",
print "...Connected!"

instanceAge = 0
refreshRate = 2.5
user_id = 0

running = True
while running:
    networkFailure = True
    while networkFailure:
        try:
            updates = atb.getUpdates(offset=newestOffset+1)
            for u in updates:
                newestOffset = u.update_id
            networkFailure = False
        except Exception:
            print "...",

    if instanceAge % (refreshRate * 10) == 0: #print 1 X every eight ticks
        print "Y"
    else:
        print "X",


    for u in updates:
        currentMessage = u.message
        try:
            user_id = currentMessage.chat.id
            parsedCommand = re.split(r'[@\s:,\'*]', currentMessage.text.lower())[0]

            running = atbCommands.process(atb, user_id, parsedCommand, currentMessage.text, currentMessage, u, instanceAge)


        except Exception as myException:
            print traceback.format_exc()
    instanceAge += refreshRate
    time.sleep(refreshRate)
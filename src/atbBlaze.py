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

from pydblite import Base #The PyDbLite stuff
import builtins

messagesSent = 0
spamLimitTime = 15

spamArray = {}

def blazestats(currentMessage):
    outputString = "JOINTS BLAZED:\n"
    K = list()
    for user in builtins.blazeDB:
        K.append(user)
    sortedK = sorted(K, key=lambda x: int(x['counter']), reverse=True)
    for user in sortedK:
        pluralString = " JOINT"
        if not(int(user["counter"]) == 1):
            pluralString += "S"
        pluralString += "\n"

        if int(user['timestamp']) + (24 * 3600) - 60 > time.mktime(currentMessage.date.timetuple()):
            outputString += "*"
        outputString += user["name"].upper() + ": " + str(user["counter"]) + pluralString

    return outputString


def blazeAM(currentMessage):
	pass

def blaze(currentMessage):
	return "Blaze 2.0 - coming Soon(tm)!"
    extraParam = False
    try:
        if currentMessage.text.lower().split()[1] == "stats":
        	return blazestats(currentMessage)
        elif currentMessage.text.lower().split()[1] == "halloffame":
        	return "BLAZE HALL OF FAME\nRachel Gentile - December 24th 2015 - 420 JOINTS"
        elif currentMessage.text.lower().split()[1] == "info":
        	returningString = "/blaze at 4:20 PM yields from 1 to 4 points. At 0 seconds it is worth 4 points and that value goes down every 15 seconds.\n"
        	returningString += "\n/blaze at 4:20 AM yields from 1 to 2 points. At 0 seconds it is worth 2 points and that value goes down every 30 seconds.\n"
        	returningString += "\nStreaks reward bonus points per day, starting at +1 for every blaze after a 3 day streak, then +1 again every 5 new days of a streak (so 3, 8, 13, etc)\n"
    		returningString += "\nThe first three people to PM blaze will get an extra +1 on top of everything else.\n"
    		returningString += "\n(the AM blaze has no effect on streaks, positive or negative.)"
    		return returningString
    except IndexError:
        extraParam = True

    start = datetime.time(4, 20)
    end = datetime.time(4, 20)

    time_received = currentMessage.date

    start2 = datetime.time(16, 20)
    end2 = datetime.time(16, 20)

    if start <= datetime.time(time_received.hour, time_received.minute) <= end: #4:20 AM

        if not checkingStats:
            return currentMessage.from_user.first_name + ", I know you like staying up late, but you really need to puff puff pass out."
    
    elif (start2 <= datetime.time(time_received.hour, time_received.minute) <= end2):
        pointsReceived = 4 - int(time_received.second / 15)

        userWasFound = False
        valueSuccessfullyChanged = False
        userPoints = 0

        for user in builtins.blazeDB:
            if int(user['username']) == currentMessage.from_user.id:
                if time.mktime(currentMessage.date.timetuple()) - 60 > int(user['timestamp']):
                    builtins.blazeDB.update(user, counter=int(user['counter']) + pointsReceived)
                    userPoints = user['counter']
                    builtins.blazeDB.update(user, timestamp=int(time.mktime(currentMessage.date.timetuple())))
                    valueSuccessfullyChanged = True
                    print("Found user!\n")
                userWasFound = True

        if not userWasFound:
            builtins.blazeDB.insert(currentMessage.from_user.id, currentMessage.from_user.first_name, pointsReceived, int(time.mktime(currentMessage.date.timetuple())))
            userPoints = pointsReceived

        if valueSuccessfullyChanged or not userWasFound:
            pluralString = " JOINT"
            if pointsReceived > 1:
                pluralString = pluralString + "S"
            return currentMessage.from_user.first_name.upper() + " 420 BLAZED IT AT " + str(time_received.second).upper() + " SECONDS. THEY BLAZED " + str(pointsReceived) + pluralString + " AND HAVE NOW SMOKED " + str(userPoints) + " IN TOTAL."
        else:
            return currentMessage.from_user.first_name + " is getting a bit too eager to blaze it."
    else:
        if not checkingStats:
            return currentMessage.from_user.first_name + " failed to blaze."

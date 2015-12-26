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

def blazestats(date):
    outputString = "BLAZE LEADERBOARD:\n"
    K = list()
    for user in builtins.blazeDB:
        K.append(user)
    sortedK = sorted(K, key=lambda x: int(x['score']), reverse=True)
    for user in sortedK:
        pluralString = " POINT"
        if not(int(user["score"]) == 1):
            pluralString += "S"
        pluralString += "\n"

        if user['topThree']:
            outputString += "+"

        if int(user['AMtimestamp']) + (24 * 3600) - 60 > time.mktime(date.timetuple()):
            outputString += "&"

        if int(user['PMtimestamp']) + (24 * 3600) - 60 > time.mktime(date.timetuple()):
            outputString += "*"

        if user['streak'] > 1:
            outputString += " (" + str(user['streak']) + ")"

        outputString += " " + user["name"].upper() + ": " + str(user["score"]) + pluralString

    return outputString

def blazePenalty(sender):
    for user in builtins.blazeDB:
        if user is not None and sender.id == int(user['id']):
            builtins.blazeDB.update(user, penalty=user['penalty'] + 1)
            if user['penalty'] > 2: # time to get penalized
                builtins.blazeDB.update(user, streak=1)
                builtins.blazeDB.update(user, score=max(0, user['score'] - 1))
                if user['score'] > 0:
                    return "PENALTY. " + sender.first_name.upper() + " HAD THEIR STREAK RESET AND LOST 1 POINT. THEY'RE NOW AT " + str(user['score']) + " POINTS."
                else:
                    return ""
            else:
                return "If " + sender.first_name + " spams /blaze " + str(3 - user['penalty']) + " more time(s), they'll get penalized."
    return sender.first_name + " failed to blaze."

def blazeAM(time_received, currentMessage):
    userWasFound = False
    valueSuccessfullyChanged = False
    pointsReceived = 0
    userPoints = 0

    pointsReceived = 2 - int(time_received.second / 30)

    for user in builtins.blazeDB:
        if int(user['id']) == currentMessage.from_user.id:
            if time.mktime(time_received.timetuple()) - 60 > int(user['AMtimestamp']):
                builtins.blazeDB.update(user, score=int(user['score']) + pointsReceived)
                builtins.blazeDB.update(user, AMtimestamp=int(time.mktime(currentMessage.date.timetuple())))
                builtins.blazeDB.update(user, penalty=0)
                userPoints = user['score']

                valueSuccessfullyChanged = True
            userWasFound = True

    if not userWasFound:
        userName = currentMessage.from_user.first_name
        userLastInitial = ""
        try:
            userLastInitial = currentMessage.from_user.last_name[0].upper()
            userName += " "
            userName += userLastInitial
        except:
            pass

        builtins.blazeDB.insert(currentMessage.from_user.id, userName, pointsReceived, int(time.mktime(currentMessage.date.timetuple())), 1, 0, 0, False)
        userPoints = pointsReceived

    if valueSuccessfullyChanged or not userWasFound:
        return currentMessage.from_user.first_name + " blazed it.\nIdk why you're awake, but you got it at " + str(time_received.second) + " seconds so here's " + str(pointsReceived) + " point(s) for your troubles.\nYou're now at " + str(userPoints) + " points total. Go to bed!"
    else:
        return blazePenalty(currentMessage.from_user)

def blazePM(time_received, currentMessage):

    userWasFound = False
    valueSuccessfullyChanged = False
    userPoints = 0
    pointsReceived = 0
    pointsReceivedFromTopThree = 0
    pointsReceivedFromStreak = 0
    topThree = False
    currentStreak = 0
    gotStreak = False

    pointsReceived += 4 - int(time_received.second / 15)

    for user in builtins.blazeDB: #search for user
        if int(user['id']) == currentMessage.from_user.id: #found them
            if time.mktime(time_received.timetuple()) - 60 > int(user['PMtimestamp']): #not twice in one minute
                #handle top three#
                builtins.blazeList.append(currentMessage.from_user.id)
                if currentMessage.from_user.id in builtins.blazeList[0:2]: #if is in first three
                    topThree = True
                    pointsReceivedFromTopThree = 1

                if topThree:
                    builtins.blazeDB.update(user, topThree=True)
                else:
                    builtins.blazeDB.update(user, topThree=False)
                #END handle top three#

                #handle streaks#
                if int(user['PMtimestamp']) + 86460 > time.mktime(time_received.timetuple()): #they did it a day ago, streak is on
                    gotStreak = True

                if gotStreak:
                    builtins.blazeDB.update(user, streak=user['streak'] + 1) #one more day of streak
                    currentStreak = user['streak']
                else: # streak is broken
                    builtins.blazeDB.update(user, streak=1)
                    currentStreak = 0

                if currentStreak >= 3:
                    currentStreak -= 3
                    pointsReceivedFromStreak += 1

                pointsReceivedFromStreak += int(currentStreak / 5) #every 5 days past 3, add one
                currentStreak += 3
                #END handle streaks#

                builtins.blazeDB.update(user, score=int(user['score']) + pointsReceived + pointsReceivedFromStreak + pointsReceivedFromTopThree)
                builtins.blazeDB.update(user, PMtimestamp=int(time.mktime(currentMessage.date.timetuple())))
                builtins.blazeDB.update(user, penalty=0)
                userPoints = user['score']

                valueSuccessfullyChanged = True
            userWasFound = True

    if not userWasFound:
        userName = currentMessage.from_user.first_name
        userLastInitial = ""
        try:
            userLastInitial = currentMessage.from_user.last_name[0].upper()
            userName += " "
            userName += userLastInitial
        except:
            pass
        builtins.blazeList.append(currentMessage.from_user.id)
        if currentMessage.from_user.id in builtins.blazeList[0:2]: #if is in first three
            topThree = True
            pointsReceivedFromTopThree = 1

        builtins.blazeDB.insert(currentMessage.from_user.id, userName, pointsReceived + pointsReceivedFromStreak + pointsReceivedFromTopThree, 0, int(time.mktime(currentMessage.date.timetuple())), 1, 0, topThree)
        userPoints = pointsReceived + pointsReceivedFromTopThree + pointsReceivedFromStreak

    if valueSuccessfullyChanged or not userWasFound:
        pluralString = " POINT"
        if userPoints > 1:
            pluralString = pluralString + "S"

        returningString = currentMessage.from_user.first_name.upper() + " BLAZED IT!\n"
        returningString += str(time_received.second).upper() + " SECONDS: +" + str(pointsReceived) + "\n"
        if pointsReceivedFromStreak > 0:
            returningString += str(currentStreak) + " DAY STREAK: +" + str(pointsReceivedFromStreak) + "\n"
        if pointsReceivedFromTopThree > 0:
            returningString += "TOP THREE! +1\n"
        returningString += "= +" + str(pointsReceived + pointsReceivedFromStreak + pointsReceivedFromTopThree) + "\n"
        returningString += "THEY NOW HAVE " + str(userPoints) + pluralString

        if str(currentMessage.chat.id) not in builtins.groupsBlazed:
            builtins.groupsBlazed += str(currentMessage.chat.id) + " "

        return returningString
    else:
        return blazePenalty(currentMessage.from_user)

def blaze(currentMessage):
    extraParam = True
    try:
        if currentMessage.text.lower().split()[1] == "stats":
            return blazestats(currentMessage.date)
        elif currentMessage.text.lower().split()[1] == "halloffame" or currentMessage.text.lower().split()[1] == "hall":
            return "BLAZE HALL OF FAME\nRachel Gentile - 12/24/2015 | 420 JOINTS"
        elif currentMessage.text.lower().split()[1] == "info":
            returningString = "/blaze at 4:20 PM yields from 1 to 4 points. At 0 seconds it is worth 4 points and that value goes down every 15 seconds.\n"
            returningString += "\n/blaze at 4:20 AM yields from 1 to 2 points. At 0 seconds it is worth 2 points and that value goes down every 30 seconds.\n"
            returningString += "\nStreaks reward bonus points per day, starting at +1 for every blaze after a 3 day streak, then +1 again every 5 new days of a streak (so 3, 8, 13, etc)\n"
            returningString += "\nThe first three people to PM blaze will get an extra +1 on top of everything else.\n"
            returningString += "\n(the AM blaze has no effect on streaks, positive or negative.)\n"
            returningString += "\n(in the leaderboard, the + means someone got top three, the * means they got the latest PM blaze, and the & means they got the latest AM blaze)"
            return returningString
    except IndexError:
        extraParam = False

    start = datetime.time(4, 20)
    end = datetime.time(4, 20)

    time_received = currentMessage.date

    start2 = datetime.time(16, 20)
    end2 = datetime.time(16, 20)

    if start <= datetime.time(time_received.hour, time_received.minute) <= end: #4:20 AM
        return blazeAM(time_received, currentMessage)

    elif (start2 <= datetime.time(time_received.hour, time_received.minute) <= end2): #4:20 PM
        return blazePM(time_received, currentMessage)
    else:
        if not extraParam:
            return blazePenalty(currentMessage.from_user)

    return "I have no idea how you got here."

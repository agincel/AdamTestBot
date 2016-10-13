#All community-made commands should go here. Write your command
#and make a pull request, and I'll try to implement it. I'll
#provide some examples here. Otherwise check out atbCommands.py
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
from threading import Thread
from urllib.request import urlopen
try:
    import psutil
except:
    pass

from .. import atbSendFunctions as atbSendFunctions
from .. import atbMiscFunctions as atbMiscFunctions
from . import atbQuote

from pydblite import Base #The PyDbLite stuff
import builtins

#If you make your own python files for processing data, put them
#In the community folder and import them here:


####

chatInstanceArray = {}

def process(bot, chat_id, parsedCommand, messageText, currentMessage, update, instanceAge):
    def sendText(givenText, replyingMessageID=0, keyboardLayout=[]):
        if not chatInstanceArray[chat_id]['adminDisable']:
            atbSendFunctions.sendText(bot, chat_id, givenText, replyingMessageID, keyboardLayout)

    def sendPhoto(imageName):
        atbSendFunctions.sendPhoto(bot, chat_id, "images/" + imageName)

    def sendSticker(stickerName):
        atbSendFunctions.sendSticker(bot, chat_id, "stickers/" + stickerName)

    def sendAudio(audioName):
        atbSendFunctions.sendAudio(bot, chat_id, "audio/" + audioName)

    def sendVideo(videoName):
        atbSendFunctions.sendVideo(bot, chat_id, "videos/" + videoName)

    def passSpamCheck(timeDelay=15):
        return atbMiscFunctions.spamCheck(chat_id, currentMessage.date, timeDelay)

    try:
        chatInstanceArray[chat_id]['checking'] = True
    except Exception:
        chatInstanceArray[chat_id] = {'checking': True, 'adminDisable': False, 'spamTimestamp': 0, 'shottyTimestamp': 0, 'shottyWinner': "", 'checkingVehicles': False, 'whoArray': []}

    try:
        #commands go here, in this if-elif block. Python doesn't have switch statements.
        if parsedCommand == "/mom": #sends "MOM GET THE CAMERA"
            sendText("MOM GET THE CAMERA")

        elif atbMiscFunctions.isMoom(parsedCommand): #sends M {random number of Os} M
            if passSpamCheck(): #use this to prevent spamming of a command
                response = "M"
                for i in range(0, random.randint(3, 75)):
                    response += "O"
                sendText(response + "M")

        elif parsedCommand == "/swag":
            sendText("swiggity swag, what\'s in the bag?")

        elif parsedCommand == "/worms":
            if passSpamCheck():
                response = "hey man can I borrow your "
                if len(messageText) > len("/worms "):
                    response += messageText[len("/worms "):]
                else:
                    response += "worms"
                sendText(response)

        elif parsedCommand == "/shh" or parsedCommand == "/shhh":
            if passSpamCheck():
                sendPhoto("shhh.jpg")

        elif parsedCommand == "/father":
            if (random.randint(0, 1)):
                sendText("You ARE the father!")
            else:
                sendText("You are NOT the father!")

        elif parsedCommand == "/rip":   #sends "I can't believe that [name (defaults to sender's name)] is fucking dead."
            if passSpamCheck():
                response = "I can't believe that "

                while "my " in messageText:
                    messageText = messageText.replace("my ", currentMessage.from_user.first_name + "\'s ", 1)

                if len(messageText) > len("/rip "):
                    if messageText[len("/rip "):] == "me":
                        response += currentMessage.from_user.first_name
                    else:
                        response += messageText[len("/rip "):]
                else:
                    response += currentMessage.from_user.first_name
                response += " is fucking dead."
                sendText(response)

        elif parsedCommand == "/rips":   #sends "I can't believe that [name (defaults to sender's name)] is fucking dead."
            if passSpamCheck():
                response = "I can't believe that "

                while "my " in messageText:
                    messageText = messageText.replace("my ", currentMessage.from_user.first_name + "\'s ", 1)

                if len(messageText) > len("/rip "):
                    if messageText[len("/rip "):] == "me":
                        response += currentMessage.from_user.first_name
                    else:
                        response += messageText[len("/rip "):]
                else:
                    response += currentMessage.from_user.first_name
                response += " are fucking dead."
                sendText(response)

        elif parsedCommand == "/scrub":
            checkingStats = False
            try:
                if currentMessage.text.lower().split()[1] == "stats":
                    db = Base('chatStorage/scrub.pdl') #The path to the DB
                    db.create('username', 'name', 'counter', mode="open")
                    K = list()
                    for user in db:
                        K.append(user)
                    sortedK = sorted(K, key=lambda x: int(x['counter']), reverse=True)
                    outputString = "SCRUBBIEST LEADERBOARD:\n"
                    for user in sortedK:
                        pluralString = " SCRUB POINT"
                        if not(int(user['counter']) == 1):
                            pluralString += "S"
                        pluralString += "\n"
                        outputString += user['name'].upper() + ": " + str(user['counter']) + pluralString
                    sendText(outputString)
                    checkingStats = True
            except IndexError:
                pass

            if not checkingStats and (currentMessage.from_user.id == 169883788 or currentMessage.from_user.id == 44961843):
                db = Base('chatStorage/scrub.pdl')
                db.create('username', 'name', 'counter', mode="open")

                userWasFound = False
                valueSuccessfullyChanged = False

                try:
                    pointsAdded = float(currentMessage.text.lower().split()[1])
                except (IndexError, ValueError):
                    pointsAdded = 1

                for user in db:
                    if int(user['username']) == currentMessage.reply_to_message.from_user.id:
                        db.update(user, counter=int(user['counter']) + pointsAdded)
                        valueSuccessfullyChanged = True
                        userWasFound = True
                db.commit()

                if not userWasFound:
                    db.insert(currentMessage.reply_to_message.from_user.id, currentMessage.reply_to_message.from_user.first_name, pointsAdded)
                    db.commit()

                if valueSuccessfullyChanged or not userWasFound:
                    sendText("Matt Gomez awarded " + str(pointsAdded) + " scrub point(s) to " + currentMessage.reply_to_message.from_user.first_name + ".")

            elif not checkingStats:
                sendText("AdamTestBot, powered by ScrubSoft (C)")

        elif parsedCommand == "/hiss":
            checkingStats = False
            try:
                if currentMessage.text.lower().split()[1] == "stats":
                    db = Base('chatStorage/hiss.pdl')
                    db.create('username', 'name', 'counter', mode="open")
                    K = list()
                    for user in db:
                        K.append(user)
                    sortedK = sorted(K, key=lambda x: int(x['counter']), reverse=True)
                    outputString = "Hiss Leaderboard:\n"
                    for user in sortedK:
                        pluralString = " hiss"
                        if not(int(user['counter']) == 1):
                            pluralString += "es"
                        pluralString += "\n"
                        outputString += user['name'] + ": " + str(user['counter']) + pluralString
                    sendText(outputString)
                checkingStats = True
            except IndexError:
                pass

            if not checkingStats and (currentMessage.from_user.id == 122526873 or currentMessage.from_user.id == 44961843):
                db = Base('chatStorage/hiss.pdl')
                db.create('username', 'name', 'counter', mode="open")

                userWasFound = False
                valueSuccessfullyChanged = False

                for user in db:
                    if int(user['username']) == currentMessage.reply_to_message.from_user.id:
                        db.update(user, counter=int(user['counter']) + 1)
                        valueSuccessfullyChanged = True
                        userWasFound = True
                db.commit()

                if not userWasFound:
                    db.insert(currentMessage.reply_to_message.from_user.id, currentMessage.reply_to_message.from_user.first_name, 1)
                    db.commit()

                if valueSuccessfullyChanged or not userWasFound:
                    sendText("Robyn hissed at " + currentMessage.reply_to_message.from_user.first_name + ".")

        elif parsedCommand == "/water":
            if passSpamCheck():
                if (random.randint(0, 1) == 0):
                    sendSticker("water.webp")
                else:
                    sendSticker("hoboken_water.webp")

        elif parsedCommand == "/sysinfo":
            if passSpamCheck():
                cpu = []
                for x in range(3):
                    cpu.append(psutil.cpu_percent(interval=1))
                cpuavg = round(sum(cpu) / float(len(cpu)), 1)
                memuse = psutil.virtual_memory()[2]
                diskuse = psutil.disk_usage('/')[3]
                sendText("The CPU uasge is " + str(cpuavg) + "%, the memory usage is " + str(memuse) + "%, and " + str(diskuse) + "% of the disk has been used.")

        elif parsedCommand == "/grill":
            if passSpamCheck():
                sendPhoto("grill.jpg")

        elif parsedCommand == "/pants":
            if passSpamCheck():
                sendText("Shit! I can't find my pants.")

        elif parsedCommand == "/broken":
            if passSpamCheck():
                if len(messageText) > len("/broken "):
                    message = str(currentMessage.from_user.username) + " says: @magomez96 my " + messageText[len("/broken "):] + " is broken!"
                else:
                    message = str(currentMessage.from_user.username) + " says: @magomez96 my shit is broken!"
                sendText(message)

        elif parsedCommand == "/quote":
            if passSpamCheck(5):
                try:
                    sendText(atbQuote.getQuoteAt(chat_id, int(messageText.split()[1])))
                except:
                    sendText(atbQuote.getQuote(chat_id))

        elif parsedCommand == "/quotefrom":
            print("\n" + messageText[len("/quotefrom "):])
            if passSpamCheck(5):
                sendText(atbQuote.getQuoteFrom(chat_id, messageText[len("/quotefrom "):]))

        elif parsedCommand == "/quoteremove":
            if currentMessage.from_user.username == "AdamZG" or currentMessage.from_user.username == "magomez96" or currentMessage.from_user.username == "Peribot":
                if atbQuote.quoteRemove(chat_id, int(messageText.split()[1])):
                    sendText("Quote " + messageText.split()[1] + " removed")
                else:
                    sendText("That quote doesn't exist or you never added any quotes")

        elif parsedCommand == "/quoteadd":
            if currentMessage.reply_to_message == None and messageText == "/quoteadd":
                sendText("Try replying to a message with this command to add it to the quote list")
            else:
                try:
                    if currentMessage.reply_to_message.from_user.first_name.lower() == 'adamtestbot':
                        sendText("Not happening")
                except:
                    pass
                userLastName = ""
                try:
                    userLastName = " " + currentMessage.from_user.last_name
                except:
                    pass
                try:
                    replyUserLastName = ""
                    try:
                        replyUserLastName = " " + currentMessage.reply_to_message.from_user.last_name
                    except:
                        replyUserLastName = ""
                    quote_resp = atbQuote.quoteAdd(chat_id, '"' + currentMessage.reply_to_message.text + '"', (currentMessage.reply_to_message.from_user.first_name + replyUserLastName).strip())
                    sendText(quote_resp)
                except(Exception):
                    quoteParse = currentMessage.text.split("-")
                    quote = "-".join(quoteParse[:-1])
                    quote = quote[len("/quoteadd "):].strip()
                    quote_resp = atbQuote.quoteAdd(chat_id, quote, quoteParse[-1].strip(), (currentMessage.from_user.first_name + userLastName).strip())
                    sendText(quote_resp)

        elif parsedCommand == "/quotelegacy":
            if passSpamCheck(5):
                sendText(atbQuote.getQuoteLegacy(chat_id))

        elif parsedCommand == "/pogo":
            def getPokeInfo():
                start = time.time()
                try:
                    nf = urlopen("https://pgorelease.nianticlabs.com/plfe/", timeout = 3)
                    page = nf.read()
                    end = time.time()
                    nf.close()
                except TimeoutError:
                    end=time.time()
                    rTime = round((end - start) * 1000)
                    if (rTime < 800):
                        sendText("Pokémon GO is UP\n{}ms Response Time".format(rTime))
                    elif (rTime >= 800 and rTime < 3000):
                        sendText("Pokémon GO's servers are struggling\n{}ms Response Time".format(rTime))
                    elif (rTime >= 3000):
                        sendText("Pokémon GO is DOWN\n{}ms Response Time".format(rTime))
                except Exception as e:
                    sendText("Pokémon GO's servers are really not doing well\nHere's what I got back\n" + e.__str__())
            
            myThread = Thread(target=getPokeInfo)
            myThread.start()

        elif parsedCommand == "/discourse":
            if passSpamCheck():
                if (random.randint(0, 1) == 0):
                    sendPhoto("discourse.jpg")
                else:
                    sendText("http://thediscour.se")

        #this command should go last:
        elif parsedCommand == "/community": #add your command to this list
            response = "/mom - get the camera\n"
            response += "/mooom (any number of \'o\'s) - call for help\n"
            response += "/swag - more memes\n"
            response += "/worms - can I borrow them?\n"
            response += "/shh(h) - here, be relaxed\n"
            response += "/father - are you the father?\n"
            response += "/rip(s) (something) - I can't believe they're dead! (The s is for plural dead things)\n"
            response += "/hiss stats - see how many time Robyn has hissed at people\n"
            response += "/scrub or /scrub stats - see who sponsors me or how many times Matt Gomez has called you a scrub\n"
            response += "/water - does this water look brown to you?\n"
            response += "/sysinfo - Gets server performance info.\n"
            response += "/grill - I'm a George Foreman grill!\n"
            response += "/pants - Pants?\n"
            response += "/broken - Tell Matt Gomez your stuff is broken.\n"
            response += "/quote - Pulls a random quote from a list. Reply to a message with /quoteadd to add one!\n"
            response += "/pogo - Want to know if Pokémon GO's servers are up?\n"
            response += "/discourse - Break in case of spicy discourse"
            sendText(response)

        else:
            return False

        return True
    except Exception:
        print(traceback.format_exc())
        return False

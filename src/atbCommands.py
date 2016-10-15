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

from . import atbSendFunctions
from . import atbMiscFunctions
from . import atbAdLib
from . import atbLikes
from . import atbBlaze
from . import atbBTC
from . import atbFirebase
from . import atbMarkov
from .Community import atbCommunity as atbCommunity

from pydblite import Base #The PyDbLite stuff
import builtins

chatInstanceArray = {}
btcInstanceArray = {}
spamLimitTime = 15
messageSent = 1


def process(bot, chat_id, parsedCommand, messageText, currentMessage, update, instanceAge):
    global messageSent

    def sendText(givenText, replyingMessageID=0, keyboardLayout=[], markdown=False):
        if not chatInstanceArray[chat_id]['adminDisable']:
            global messageSent
            messageSent += 1
            atbSendFunctions.sendText(bot, chat_id, givenText, replyingMessageID, keyboardLayout, markdown=markdown)

    def sendPhoto(imageName):
        global messageSent
        messageSent += 1
        atbSendFunctions.sendPhoto(bot, chat_id, "images/" + imageName)

    def sendSticker(stickerName):
        global messageSent
        messageSent += 1
        atbSendFunctions.sendSticker(bot, chat_id, "stickers/" + stickerName)

    def passSpamCheck(timeDelay=15):
        return atbMiscFunctions.spamCheck(chat_id, currentMessage.date, timeDelay)

    try:
        atbMiscFunctions.log(chat_id, currentMessage)

        try:
            chatInstanceArray[chat_id]['checking'] = True
        except Exception:
            chatInstanceArray[chat_id] = {'checking': True, 'adminDisable': False, 'spamTimestamp': 0, 'shottyTimestamp': 0, 'shottyWinner': "", 'checkingVehicles': False, 'whoArray': [], 'lobbyList': list()}

        try:
            btcInstanceArray[chat_id]['checking'] = True
        except Exception:
            btcInstanceArray[chat_id] = {'checking': True, 'shopType': "upgrades", 'shopPage': 0, 'buyingItem': "", 'itemTarget': "", 'enteringTarget': False}

        if parsedCommand == "/admin":
            if currentMessage.from_user.username == "AdamZG":
                try:
                    if messageText.lower().split()[1] == "disable":
                        chatInstanceArray[chat_id]['adminDisable'] = True
                        sendText("Adam has disabled me.")
                    elif messageText.lower().split()[1] == "enable":
                        chatInstanceArray[chat_id]['adminDisable'] = False
                        sendText("Adam has enabled me.")
                    elif messageText.lower().split()[1] == "sendto":
                        atbSendFunctions.sendText(bot, int(messageText.lower().split()[2]), messageText[15 + len(messageText.split()[2]):])
                    elif messageText.lower().split()[1] == "blaze":
                        bot.sendDocument(chat_id=-12788453, document=open("chatStorage/blaze.pdl", "rb"))
                    elif messageText.lower().split()[1] == "update":
                        try:
                            atbFirebase.update()
                        except:
                            print(traceback.format_exc())
                        sendText("Site updated.")
                except Exception:
                    pass

        elif messageText.lower().startswith("@adamtestbot"):
            sendText(atbMiscFunctions.atReply())

        elif parsedCommand == "/whodefine":
            if atbAdLib.whoDefine(chat_id, messageText):
                sendText("Entries stored to file.")
            else:
                sendText("Entries cleared. Define new array before using /who")

        elif parsedCommand == "/whoadd":
            if atbAdLib.whoAdd(chat_id, messageText):
                sendText("Entries stored to file.")
            else:
                sendText("USAGE: /whoadd Name or /whoadd Name, Name...")

        elif parsedCommand == "/whocoulditbe":
            sendText(atbAdLib.whoCouldItBe(chat_id))

        elif parsedCommand == "/like":
            atbLikes.handleLikes(True, currentMessage)

        elif parsedCommand == "/lile" or parsedCommand == "/kek":
            atbLikes.handleLikes(True, currentMessage)
            if passSpamCheck():
                sendText("I guess " + parsedCommand + " is close enough.")

        elif parsedCommand == "/dislike":
            atbLikes.handleLikes(False, currentMessage)

        elif parsedCommand == "/likes":
            sendText(atbLikes.likes(currentMessage))

        elif parsedCommand == "/vehicles" and (currentMessage.from_user.id == 51561968 or currentMessage.from_user.id == 44961843):
            chatInstanceArray[chat_id]['checkingVehicles'] = True
            sendText("Do you like vehicles?", keyboardLayout=[["they\'re okay"], ["I FUCKING LOVE VEHICLES"], ["they\'re okay"], ["they\'re okay"]])

        #normal commands go here

        elif parsedCommand == "/ping":
            sendText("pong")

        elif parsedCommand == "/expand":
            sendText("dong")

        elif parsedCommand == "/meme":
            sendText("get memed on")

        elif parsedCommand == "/john_madden":
            sendText("aeiou")

        elif parsedCommand == "/john_cena":
            if passSpamCheck():
                sendText("ARE YOU READY FOR THIS SUNDAY NIGHT WHEN WWE CHAMP JOHN CENA DEFENDS HIS TITLE IN THE WWE SUUUUUUPERSLAMMMMMMM")
                sendText("right now you can order this awesome pay per view event for just $59.99")

        elif parsedCommand == "/message" and currentMessage.from_user.id == 44961843:
            builtins.blazeMessage = messageText[len("/message "):]
            sendText("Message received.")

        elif parsedCommand == "/motd":
            sendText(builtins.blazeMessage)

        elif parsedCommand == "/markov":
            if passSpamCheck(30) or currentMessage.from_user.id == 44961843:
                sendText(atbMarkov.getMarkov(messageText))

        elif parsedCommand == "/blaze" and chat_id != 106128903:
            sendText(atbBlaze.blaze(currentMessage))

        elif parsedCommand == "/blazecommit" and currentMessage.from_user.id == 44961843:
            builtins.blazeDB.commit()

        elif parsedCommand == "/blazeopen" and currentMessage.from_user.id == 44961843:
            builtins.blazeDB = Base('chatStorage/blaze.pdl') #The path to the database
            builtins.blazeDB.create('username', 'name', 'counter', 'timestamp', mode="open") #Create a new DB if one doesn't exist. If it does, open it

        elif parsedCommand == "/snail":
            sendText(atbMiscFunctions.snailResponse(messageText))

        elif parsedCommand == "/essay":
            sendText(random.choice(["NO. FUCK ESSAYS.", "I DON\'T WANNA."]))

        elif parsedCommand == "/kevi" + "\xC3\xB1":
            if passSpamCheck():
                sendPhoto("kevin.jpg")

        elif parsedCommand == "/bitch":
            if passSpamCheck():
                sendPhoto("engling.jpg")

        elif parsedCommand == "/smash":
            sendText(atbMiscFunctions.smashCommand())

        elif parsedCommand == "/screams":
            if passSpamCheck():
                sendText(currentMessage.from_user.first_name + ": " + atbMiscFunctions.screamsCommand())

        elif parsedCommand == "/summon":
            sendText(atbMiscFunctions.summonResponse(currentMessage))

        elif parsedCommand == "/pick":
            sendText(atbMiscFunctions.pickResponse(messageText))

        elif parsedCommand == "/lobby":
            name = currentMessage.from_user.first_name
            try:
                name += " " + currentMessage.from_user.last_name[0].upper() + "."
            except:
                pass
            if messageText == "/lobby":
                if [name, currentMessage.from_user.id] in chatInstanceArray[chat_id]['lobbyList']:
                    chatInstanceArray[chat_id]['lobbyList'].remove([name, currentMessage.from_user.id])
                else:
                    chatInstanceArray[chat_id]['lobbyList'].append([name, currentMessage.from_user.id])
            elif messageText == "/lobby close" or messageText == "/lobby exit" or messageText == "/lobby leave" or messageText == "/lobby clear":
                    chatInstanceArray[chat_id]['lobbyList'] = list()
            outputString = "```\nLobby:\n"
            for user in chatInstanceArray[chat_id]['lobbyList']:
                outputString += "\t" + user[0] + "\n"
            outputString += "----------------\n'/lobby show' displays the Lobby\n'/lobby leave' clears it```"
            if passSpamCheck(5) or messageText == "/lobby show":
                sendText(outputString, markdown=True)

        elif parsedCommand == "/markdown":
            bot.sendMessage(chat_id=chat_id, text="```\nLook at this beautiful\nMONOSPACE```", parse_mode="Markdown")

        elif parsedCommand == "/fmk":
            sendText(atbMiscFunctions.fmk(re.split(r'[@\s*]', messageText[len("/fmk "):])))

        elif parsedCommand == "/scale":
            splitText = re.split(r'[@\s:,\'*]', currentMessage.text.lower())
            output = ""
            if len(splitText) < 3:
                output = "USAGE: '/scale a b'"
            else:
                try:
                    low = int(splitText[1])
                    high = int(splitText[2])
                    ret = 0
                    if low < high:
                        ret = random.randrange(low, high + 2)
                    elif low > high:
                        ret = random.randrange(high, low + 2)
                    else:
                        ret = low

                    if random.randrange(1, 100) == 57:
                        ret += 1
                    output = str(ret)
                except:
                    output = "USAGE: '/scale a b' where a and b are numbers"
            sendText(output)

        elif parsedCommand == "/fight":
            sendText(atbMiscFunctions.fightResponse(currentMessage))

        elif parsedCommand == "/age":
            sendText("This instance has been running for " + atbMiscFunctions.ageCommand(instanceAge.total_seconds()) + " and has sent " + str(messageSent) + " messages!")

        elif parsedCommand == "/yesorno":
            x = random.randint(0, 1)
            if x == 0:
                sendText("No.")
            else:
                sendText("Yes.")

        elif parsedCommand == "/gtg":
            sendText(currentMessage.from_user.first_name + "\'s mom is here; they have to go.")

        elif parsedCommand == "/yiss":
            if passSpamCheck():
                sendText("aww")
                sendText("yiss")
                sendText("motha")
                sendText("fuckin")
                if len(messageText) > len("/yiss "):
                    sendText(messageText[len("/yiss "):])
                else:
                    sendText("breadcrumbs")

        elif parsedCommand == "/objection":
            sendText(atbMiscFunctions.objectionResponse(currentMessage), replyingMessageID=currentMessage.reply_to_message.message_id)

        elif parsedCommand == "/goodnight":
            sendText("Good night, " + currentMessage.from_user.first_name + "! " + telegram.emoji.Emoji.SLEEPING_FACE)

        elif parsedCommand == "/goodmorning":
            time_received = currentMessage.date
            actual_time = datetime.time(time_received.hour, time_received.minute)

            if actual_time < datetime.time(12, 0) and actual_time > datetime.time(4, 59):
                sendText("Good morning, " + currentMessage.from_user.first_name + "! " + telegram.emoji.Emoji.SMILING_FACE_WITH_OPEN_MOUTH)
            elif actual_time == datetime.time(3, 0):
                sendText(currentMessage.from_user.first_name + ": Oh boy, three AM!")
            elif actual_time <= datetime.time(4, 59):
                sendText("It's the middle of the night, " + currentMessage.from_user.first_name + "! Go to bed!")
            else:
                sendText(currentMessage.from_user.first_name + "\'s a lazy shit. It isn\'t morning anymore! " + telegram.emoji.Emoji.WEARY_FACE)

        elif parsedCommand == "/8ball":
            if currentMessage.from_user.id == 68536910:
                sendText(telegram.emoji.Emoji.SPARKLING_HEART)
            else:
                sendText(atbMiscFunctions.eightBall())

        elif parsedCommand == "/debug":
            sendText("ID: " + str(chat_id))

        elif parsedCommand == "/shotty":
            if time.mktime(currentMessage.date.timetuple()) - 3600 > chatInstanceArray[chat_id]['shottyTimestamp']:
                chatInstanceArray[chat_id]['shottyTimestamp'] = time.mktime(currentMessage.date.timetuple())
                chatInstanceArray[chat_id]['shottyWinner'] = currentMessage.from_user.first_name
                sendText(chatInstanceArray[chat_id]['shottyWinner'] + " called shotgun. Dibs no blitz for the next hour.")
            else:
                timeRemaining = int(chatInstanceArray[chat_id]['shottyTimestamp'] - (time.mktime(currentMessage.date.timetuple()) - 3600)) / 60 + 1
                sendText(chatInstanceArray[chat_id]['shottyWinner'] + " has shotty for the next " + str(timeRemaining) + " minutes.")

        elif parsedCommand == "/btc":
            result = atbBTC.handleBTC(bot, chat_id, parsedCommand, messageText, currentMessage, update, instanceAge, btcInstanceArray[chat_id])
            print(btcInstanceArray[chat_id]['shopPage'])
            if result != []:
                if result[1] == "markdown":
                    sendText(result[0], markdown=True)
                elif result[1] == "keyboard":
                    sendText(result[0], markdown=True, keyboardLayout=result[2])
                elif result[1] == "keyboardnm":
                    sendText(result[0], markdown=False, keyboardLayout=result[2])
                elif result[1] == "no":
                    pass
                else:
                    sendText(result[0])

        elif parsedCommand == "/help":
            sendText(atbMiscFunctions.helpResponse())

        elif parsedCommand == "/adlib":
            sendText(atbMiscFunctions.adlibResponse())

        elif parsedCommand == "/more":
            sendText(atbMiscFunctions.moreResponse())

        elif atbAdLib.is_valid_text_overwrite(messageText): #all adlibbing logic done here
            sendText(atbAdLib.overwrite_response(messageText, currentMessage.from_user.first_name, chat_id))

        elif parsedCommand[0] != "/" and parsedCommand[0] != "@": #normal text
            if chatInstanceArray[chat_id]['checkingVehicles']:
                if messageText.lower() == "they\'re okay":
                    sendText("You disgust me, " + currentMessage.from_user.first_name, replyingMessageID=currentMessage.message_id)
                    chatInstanceArray[chat_id]['checkingVehicles'] = False
                elif messageText.lower() == "i fucking love vehicles":
                    sendText("FUCKIN RIGHT YOU DO, " + currentMessage.from_user.first_name.upper(), replyingMessageID=currentMessage.message_id)
                    chatInstanceArray[chat_id]['checkingVehicles'] = False
            elif btcInstanceArray[chat_id]['enteringTarget']:
                result = atbBTC.handleBTC(bot, chat_id, parsedCommand, "/btc target " + messageText, currentMessage, update, instanceAge, btcInstanceArray[chat_id])

        else:
            if not atbCommunity.process(bot, chat_id, parsedCommand, messageText, currentMessage, update, instanceAge):
                pass

        if chat_id < 0: #only listen to group chats
            atbMarkov.processText(messageText)

        return True
    except Exception:
        print(traceback.format_exc())
        return True

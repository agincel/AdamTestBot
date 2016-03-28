#all the stuff related to Bot₵oin
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

from . import atbSendFunctions
from . import atbMiscFunctions

def handleBTC(bot, chat_id, parsedCommand, messageText, currentMessage, update, instanceAge, btcInstanceArray):
    def sendText(givenText, replyingMessageID=0, keyboardLayout=[]):
        atbSendFunctions.sendText(bot, chat_id, givenText, replyingMessageID, keyboardLayout)

    def sendTextTo(givenText, recipientMessageID):
        atbSendFunctions.sendText(bot, recipientMessageID, givenText, 0, [])

    def sendPhoto(imageName):
        atbSendFunctions.sendPhoto(bot, chat_id, "images/" + imageName)

    def sendSticker(stickerName):
        atbSendFunctions.sendSticker(bot, chat_id, "stickers/" + stickerName)

    def passSpamCheck(timeDelay=15):
        return atbMiscFunctions.spamCheck(chat_id, currentMessage.date, timeDelay)

    messageText.replace("@AdamTestBot", "")
    messageText.replace("@TestAdamTestBot", "")
    messageText.replace("@", "")
    newCommand = re.split(r'[@\s:,\'*]+', messageText[len("/btc"):].lstrip())
    strBtc = "Bt₵"
    strBotCoin = "Bot₵oin Beta"
    strPerHour = "⁄hr"

    def floatRound(fuck):
        return round(fuck, 3)

    def getLedger(keyField='myYield'):
        outputString = "```\n" + strBotCoin + " Ledger:\n"
        K = list()
        for user in builtins.btcDB:
            K.append(user)
        sortedK = sorted(K, key=lambda x: float(x[keyField]), reverse=True)
        for user in sortedK:
            outputString += user['username'] + " (" + user['name'] + ")\n\t" + str((round(user['money'], 3))) + strBtc + " - " 
            if float(user['positiveYields']) > 0:
                outputString += "(" + str(user['positiveMultiplier']) + "x) "
            if float(user['zeroYields']) > 0:
                outputString += "(0x) "
            if float(user['negativeYields']) > 0:
                outputString += "(" + str(user['negativeMultiplier']) + "x) "

            outputString += str(user['myYield']) + strBtc + "⁄hr\n"
        return outputString + "----------------\nType '/btc help' in a private chat with me to play!```"

    def getUser(userID):
        for user in builtins.btcDB:
            if int(user['id']) == int(userID):
                return user
        return None

    def getUserByUsername(userName):
        for user in builtins.btcDB:
            if user['username'] == userName:
                return user
        return None

    def getHelp():
        outputString = "```\n" + strBotCoin + " Help:\n"
        outputString += "/btc        | Ledger sorted by yield\n"
        outputString += "/btc list   | Ledger sorted by money\n"
        outputString += "/btc join   | Join the " + strBotCoin + " Ledger\n"
        outputString += "/btc intro  | Rules and description\n"
        outputString += "/btc shop   | Buy items\n"
        outputString += "/btc pay    | pay another user\n"
        outputString += "/btc remove | leave the game :("

        return outputString + "```"

    def getIntro():
        outputString = "Welcome to " + strBotCoin + "!\n\n"
        outputString += "This game is a progression game, in the vein of Cookie Clicker or Bitcoin Billionaire.\n"
        outputString += "Every hour, on the hour, your yield is added to your total. You start with 1.0" + strBtc + " and a yield of 0.1" + strBtc + " per hour.\n"
        outputString += "Typing '/btc shop' will let you browse the shop, and will let you buy permanent upgrades, consumable boosts, or weapons to attack others."

        return outputString

    def getItemInfo(itemName):
        info = ["Name", 999, "category", 0.0]
        if itemName == "Toothpick":
            info = ["Toothpick", 2, "upgrade", 0.025]
        elif itemName == "Nothing":
            info = ["Nothing", 0, "upgrade", 0]
        elif itemName == "Q-Tip":
            info = ["Q-Tip", 0.1, "upgrade", 0.001]
        elif itemName == "Chisel":
            info = ["Chisel", 75.0, "upgrade", 1.25]
        elif itemName == "Steroid":
            info = ["Steroid", floatRound(getUser(currentMessage.from_user.id)['myYield'] * 0.8), "consumable", 2]
        else:
            return []
        if info[2] == "upgrade":
            return [info[0] + " (+" + str(round(float(info[3]), 3)) + " " + strPerHour + "): " + str(floatRound(float(info[1]))) + strBtc + "\n", info[1], info[2], info[3]]
        elif info[2] == "consumable":
            return [info[0] + " (yield x" + str(info[3]) + "): " + str(info[1]) + strBtc + "\n", info[1], info[2], info[3]]
        else:
            return []

    def shop(newCommand):
        returnText = ""
        returnMessageType = "keyboard"
        keyboardLayout = []
        if len(newCommand) == 1:
            returnText = "Welcome to the shop! You have " + str(round(float(getUser(currentMessage.from_user.id)['money']), 3)) + strBtc + ".\n"
            returnText += "What kind of item do you want to buy?\n\n"
            returnText += "(Tip: you can type '/btc buy itemName x' where x is the number of that item you want)"
            keyboardLayout = [["/btc shop upgrades"], ["/btc shop consumables"], ["/btc shop weapons"]]
        else:
            if newCommand[1] == "upgrades":
                returnText = "Upgrades! Page 1:\n"
                returnText += getItemInfo("Q-Tip")[0]
                returnText += getItemInfo("Toothpick")[0]
                returnText += getItemInfo("Chisel")[0]
                buy = "/btc buy "
                keyboardLayout.append([buy + "Q-Tip 1"])
                keyboardLayout.append([buy + "Toothpick 1"])
                keyboardLayout.append([buy + "Chisel 1"])
                keyboardLayout.append(["/btc exit"])
            elif newCommand[1] == "consumables":
                returnText = "Consumables! Page 1:\n"
                returnText += getItemInfo("Steroid")[0]
                buy = "/btc buy "
                keyboardLayout.append([buy + "Steroid"])
                keyboardLayout.append(["/btc exit"])
            else:
                returnText = "Sorry! Not implemented yet."
                returnMessageType = ""
                
        return [returnText, returnMessageType, keyboardLayout]

    def buy(newCommand):
        if len(newCommand) > 1: #buying something
            itemInfo = getItemInfo(newCommand[1])
            quantity = 1
            try:
                quantity = int(newCommand[-1])
            except:
                pass
            if quantity < 0:
                quantity *= -1

            quantityPurchased = 0
            if itemInfo != []:
                user = getUser(currentMessage.from_user.id)
                if float(itemInfo[1]) * quantity > float(user['money']):
                    quantity = int(float(user['money'])/float(itemInfo[1]))
                if float(user['money']) >= float(itemInfo[1]) * quantity and quantity != 0: #can afford
                    quantityPurchased = quantity
                else:
                    return ["Come back when you're a little mmmm...richer.", ""]
                if itemInfo[2] == "upgrade":
                    builtins.btcDB.update(user, money=user['money'] - (itemInfo[1] * quantity))
                    builtins.btcDB.update(user, myYield=round(user['myYield'] + (itemInfo[3] * quantity), 3))
                    builtins.btcDB.commit()
                    return ["You bought " + str(quantityPurchased) + " " + newCommand[1] + "(s)!\nYour yield is now " + str(user['myYield']) + strBtc + strPerHour+ "\nYou now have " + str(round(user['money'], 3)) + strBtc + ".", ""]
                elif itemInfo[2] == "consumable":
                    if user['positiveYields'] == 0:
                        builtins.btcDB.update(user, money=user['money'] - itemInfo[1])
                        builtins.btcDB.update(user, positiveMultiplier=itemInfo[3])
                        builtins.btcDB.update(user, positiveYields=1)
                        builtins.btcDB.commit()
                        return ["You bought a " + newCommand[1] + ". Your next yield will be multiplied by " + str(itemInfo[3]) + ", making it " + str(floatRound(user['myYield'] * itemInfo[3])) + strBtc + ". You now have " + str(user['money']) + strBtc + ".", ""]
                    else:
                        return ["You already have a consumable active.", ""]
                
            else:
                return ["Invalid item name.", ""]
        else:
            return ["What're you buyin', stranger?", ""]

    def pay(newCommand):
        if len(newCommand) != 3:
            return ["USAGE: '/btc pay username amount'", ""]
        user = getUser(currentMessage.from_user.id)
        payToUser = getUserByUsername(str(newCommand[1]))
        try:
            amount = round(float(newCommand[2]), 3)
        except:
            return ["I couldn't parse " + str(newCommand[2]) + " as an amount of money.", ""]

        if payToUser == None:
            return ["I couldn't find " + str(newCommand[1]) + " on my ledger.", ""]
        elif amount > float(user['money']):
            return ["You can't afford to give that kind of money away, " + user['name'] + ".", ""]
        elif amount < 0:
            return ["I'm afraid only you can repay your debt, " + user['name'] + ".", ""]
        elif amount == 0:
            return ["How helpful. " + user['name'] + " is paying " + payToUser['name'] + " nothing.", ""]
        else:
            builtins.btcDB.update(user, money=user['money'] - amount)
            builtins.btcDB.update(payToUser, money=payToUser['money'] + amount)
            builtins.btcDB.commit()
            if int(payToUser['chat_id']) != 0:
                sendTextTo(user['name'] + " paid you " + str(amount) + strBtc + ".", int(payToUser['chat_id']))
            if int(user['chat_id']) != 0:
                sendTextTo("You paid " + payToUser['name'] + " " + str(amount) + strBtc + ".", int(user['chat_id']))
            return [user['name'] + " has paid " + payToUser['name'] + " " + str(amount) + strBtc + ".", ""]

    def updateUserChat(userID, chat_id):
        for user in builtins.btcDB:
            if int(user['id']) == int(userID) and int(chat_id) != int(user['chat_id']):
                builtins.btcDB.update(user, chat_id=int(chat_id))
                builtins.btcDB.commit()



    # -------- end helper function declarations ------- #

    if newCommand[0] == '' and int(chat_id) < 0:
        return ["Check the Ledger by typing /btc in a private chat with me. Join " + strBotCoin + " by typing '/btc join'!", ""]
    elif newCommand[0] == 'list':
        return [getLedger("money"), "markdown"]
    elif newCommand[0] == "join":
        if getUser(currentMessage.from_user.id) == None:
            username = currentMessage.from_user.username
            if username == "":
                username = currentMessage.from_user.first_name + str(int(currentMessage.from_user.id / 100000))
            name = currentMessage.from_user.first_name
            userLastInitial = ""
            try:
                userLastInitial = currentMessage.from_user.last_name[0].upper()
                name += " " + userLastInitial
            except:
                pass
            builtins.btcDB.insert(currentMessage.from_user.id, username, name, 1.0, 0.1, 0, 0, -1, 0, 0, 0, 000000)
            builtins.btcDB.commit()
            return [name + " has joined " + strBotCoin + "!\nType '/btc help' in a private chat with me to get started.", ""]
        else:
            return [currentMessage.from_user.first_name + ", you're already on the ledger.", ""]
    elif newCommand[0] == "pay":
            return pay(newCommand)
    elif getUser(currentMessage.from_user.id) == None:
        return ["Type '/btc join' to play " + strBotCoin + "!", ""]
    if int(chat_id) > 0: # if we're in a private chat
        try:
            print(newCommand)
        except:
            pass

        updateUserChat(currentMessage.from_user.id, chat_id) # make sure we know their chat_id

        if newCommand[0] == "":
            return [getLedger(), "markdown"]
        elif newCommand[0] == "help":
            return [getHelp(), "markdown"]
        elif newCommand[0] == "intro":
            return [getIntro(), ""]
        elif newCommand[0] == "shop":
            return shop(newCommand)
        elif newCommand[0] == "buy":
            return buy(newCommand)
        elif newCommand[0] == "exit":
            return ["Bye!", ""]
        elif newCommand[0] == "commit" and currentMessage.from_user.username == "AdamZG":
            builtins.btcDB.commit()
            return ["Committed the BTC database.", ""]
        elif newCommand[0] == "debug" and currentMessage.from_user.username == "AdamZG":
            print(getUserByUsername("AdamZG")['stocks'])
            return ["Printed the thing?", ""]
        elif newCommand[0] == "migrate" and currentMessage.from_user.username == "AdamZG":
            defaultStockArray = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0}
            for user in builtins.btcDB:
                builtins.btcDB1.insert(user['id'], user['username'], user['name'], user['money'], user['myYield'], user['positiveMultiplier'], user['positiveYields'], user['zeroMultiplier'], user['zeroYields'], user['negativeMultiplier'], user['negativeYields'], user['chat_id'], defaultStockArray, {})
            builtins.btcDB1.commit()
            return ["Migrated.", ""]
        elif newCommand[0] == "remove":
            builtins.btcDB.delete(getUser(currentMessage.from_user.id))
            return["Sorry to see you go. :(", ""]
    else:
        print("Not valid private chat command.")
        return ["", "no"]






#('id', 'username', 'name', 'money', 'myYield', 'positiveMultiplier', 'positiveYields', 'zeroMultiplier', 'zeroYields', 'negativeMultiplier', 'negativeYields', 'chat_id')

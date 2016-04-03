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
    strPerShare = "⁄share"

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

    def getStockBySymbol(sym):
        for stock in builtins.btcStockDB:
            if stock['letter'] == sym:
                return stock
        return None

    def defineStocks():
        #'name', 'description', 'letter', 'fullRange', 'subRangeSize', 'selectedSubRangeStart', 'currentValue', 'history', 'forecast'
        haveDoneThis = False
        for stock in builtins.btcStockDB:
            if stock['letter'] == 'A':
                haveDoneThis = True
        if not haveDoneThis:
            builtins.btcStockDB.insert("ATB Industrial Average", "The average of all other traded stocks.", 'A', [0,0], 0, 0, 10, [], True)
            builtins.btcStockDB.insert("Blaze Corp.", "Legal in Colorado.", 'B', [-.2, 0], 0.23, 0, 4.20, [], True)
            builtins.btcStockDB.insert("Consistent Co.", "A slow but safe investment.", 'C', [-0.05, 0.1], 0.05, 0, 12.25, [], True)
            builtins.btcStockDB.insert("Deez Nutz Ltd.", "High risk, high reward.", 'D', [-1, 0], 1, -4, 30, [], True)
            builtins.btcStockDB.insert("ScrubSoft Inc.", "/scrub 999999999", 'S', [-0.23, 0.15], 0.1, 0, 6.66, [], True)

    def getStockInfo(sym):
        stock = getStockBySymbol(sym)
        outputString = "Stock " + sym + ":\n"
        outputString += "Name: " + stock['name'] + "\n"
        outputString += "Desc: " + stock['description'] + "\n"
        outputString += "Symbol: " + stock['letter'] + "\n"
        outputString += "Full Range: " + str(stock['fullRange']) + '\n'
        outputString += "subRangeSize: " + str(stock['subRangeSize']) + '\n'
        outputString += "Current Subrange Start: " + str(stock['selectedSubRangeStart']) + '\n'
        outputString += "Current Value: " + str(stock['currentValue']) + '\n'
        outputString += "Forecast: " + str(stock['forecast']) + '\n'
        totalOut = 0
        for user in builtins.btcDB:
            totalOut += user['stocks'][sym]
        outputString += "Total Sold: " + str(totalOut) + '\n'
        return [outputString, ""]

    def updateStockRange(sym, low, high):
        stock = getStockBySymbol(sym)
        newRange = [low, high]
        builtins.btcStockDB.update(stock, fullRange=newRange)
        return ["Set Stock " + sym + "'s Range to " + str(newRange), ""]

    def updateStockRangeSize(sym, size):
        stock = getStockBySymbol(sym)
        builtins.btcStockDB.update(stock, subRangeSize=size)
        return ["Set Stock " + sym + "'s subRangeSize to " + str(size), ""]

    def updateStocks():
        stockValueTotal = 0
        stockNum = 0
        stockA = -1
        for stock in builtins.btcStockDB:
            if stock['letter'] != 'A':
                stockNum += 1
                stockValueTotal += stock['currentValue']
                lowerBound = stock['selectedSubRangeStart']
                builtins.btcStockDB.update(stock, selectedSubRangeStart=round(random.uniform(stock['fullRange'][0], stock['fullRange'][1]), 2))
                upperBound = stock['subRangeSize'] + lowerBound
                delta = round(random.uniform(lowerBound, upperBound), 2)
                forecastUp = True
                if abs(stock['selectedSubRangeStart']) > abs(stock['selectedSubRangeStart'] + stock['subRangeSize']):
                    forecastUp = False
                currentHistory = stock['history']

                builtins.btcStockDB.update(stock, currentValue=round(max(stock['currentValue'] + delta, 2.5), 3))
                builtins.btcStockDB.update(stock, forecast=forecastUp)

                currentHistory.append(stock['currentValue'])
                builtins.btcStockDB.update(stock, history=currentHistory)
            else:
                stockA = stock
        currentHistory = stockA['history']
        builtins.btcStockDB.update(stockA, currentValue=round((stockValueTotal / stockNum), 2))
        currentHistory.append(stockA['currentValue'])
        builtins.btcStockDB.update(stockA, history=currentHistory)
        builtins.btcStockDB.commit()

    def stockQuote():
        outputString = "```\n" + strBotCoin + " Stock Quote:\n"
        K = list()
        for stock in builtins.btcStockDB:
            K.append(stock)
        sortedK = sorted(K, key=lambda x: x['letter'], reverse=False)
        for stock in sortedK:
            outputString += stock['name'] + "\n\t"
            outputString += stock['description'] + "\n\t\t"
            outputString += str(stock['currentValue']) + strBtc + " ["
            if stock['letter'] == 'A':
                outputString += "-"
            elif stock['forecast']:
                outputString += "↑"
            else:
                outputString += "↓"
            outputString += "]\n"
        return outputString + "--------------------\nType '/btc quote' for a quote, or go to '/btc shop' to buy/sell Stocks!```"

    def getPortfolio(dialog=False):
        outputString = "```\nYour Stock Portfolio:\n"
        user = getUser(currentMessage.from_user.id)
        K = list()
        for stock in builtins.btcStockDB:
            K.append(stock)
        sortedK = sorted(K, key=lambda x: x['letter'], reverse=False)
        for stock in sortedK:
            forecast = "↓"
            if stock['letter'] == 'A':
                forecast = "-"
            elif stock['forecast']:
                forecast = "↑"
            outputString += stock['name'] + " (" + stock['letter'] + ") [" + forecast + "]\n\t"
            outputString += str(stock['currentValue']) + strBtc + strPerShare + " - " + str(user['stocks'][stock['letter']]) + " (" + str(round(stock['currentValue'] * user['stocks'][stock['letter']], 2)) + ")\n"
        if dialog:
            return outputString + "--------------\nWhat Stock Symbol do you want to manage?```"
        else:
            return outputString + "```"

    def getMe():
        user = getUser(currentMessage.from_user.id)
        outputString = "```\n"
        outputString += user['username'] + " (" + user['name'] + ")\n\t"
        outputString += str(floatRound(user['money'])) + strBtc + " - "
        if float(user['positiveYields']) > 0:
            outputString += "(" + str(user['positiveMultiplier']) + "x) "
        if float(user['zeroYields']) > 0:
            outputString += "(0x) "
        if float(user['negativeYields']) > 0:
            outputString += "(" + str(user['negativeMultiplier']) + "x) "
        outputString += str(user['myYield']) + strBtc + strPerHour + "\n\n"
        K = list()
        for stock in builtins.btcStockDB:
            K.append(stock)
        sortedK = sorted(K, key=lambda x: x['letter'], reverse=False)
        for stock in sortedK:
            if user['stocks'][stock['letter']] > 0:
                forecast = "↓"
                if stock['forecast']:
                    forecast = "↑"
                outputString += stock['name'] + " (" + stock['letter'] + ") [" + forecast + "]\n\t"
                outputString += str(stock['currentValue']) + strBtc + strPerShare + " - " + str(user['stocks'][stock['letter']]) + " (" + str(round(stock['currentValue'] * user['stocks'][stock['letter']], 2)) + strBtc + ")\n"
        return outputString + "```"

    def getHelp():
        outputString = "```\n" + strBotCoin + " Help:\n"
        outputString += "/btc        | Ledger sorted by yield\n"
        outputString += "/btc me     | Information about you\n"
        outputString += "/btc list   | Ledger sorted by money\n"
        outputString += "/btc join   | Join the " + strBotCoin + " Ledger\n"
        outputString += "/btc intro  | Rules and description\n"
        outputString += "/btc shop   | Buy items\n"
        outputString += "/btc quote  | Quote stocks\n"
        outputString += "/btc portfolio | Your stocks\n"
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
        elif itemName == "Pickaxe":
            info = ["Pickaxe", 200.0, "upgrade", 3.5]
        elif itemName == "Jackhammer":
            info = ["Jackhammer", 2500.0, "upgrade", 50]
        elif itemName == "Steroid":
            info = ["Steroid", floatRound(getUser(currentMessage.from_user.id)['myYield'] * 0.8), "consumable", 2]
        elif itemName == "Hammer":
            info = ["Hammer", "1.1x Target's Yield", "weapon", 1.1, 0]
        elif itemName == "Crowbar":
            info = ["Crowbar", "1.5x Target's Yield", "weapon", 1.5, -0.5]
        else:
            return []
        if info[2] == "upgrade":
            return [info[0] + " (+" + str(round(float(info[3]), 3)) + " " + strPerHour + "): " + str(floatRound(float(info[1]))) + strBtc + "\n", info[1], info[2], info[3]]
        elif info[2] == "consumable":
            return [info[0] + " (yield x" + str(info[3]) + "): " + str(info[1]) + strBtc + "\n", info[1], info[2], info[3]]
        elif info[2] == "weapon":
            outputString = info[0] + " (yield x " + str(info[4]) + "): " + info[1]
            return [outputString, info[1], info[2], info[3], info[4]] #desc, useless, category, multiplier, effect
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
            keyboardLayout = [["/btc shop upgrades", "/btc shop consumables"], ["/btc shop weapons", "/btc shop stocks"], ["/btc exit"]]
        else:
            if newCommand[1] == "upgrades":
                returnText = "Upgrades! Page 1:\n"
                returnText += getItemInfo("Q-Tip")[0]
                returnText += getItemInfo("Toothpick")[0]
                returnText += getItemInfo("Chisel")[0]
                returnText += getItemInfo("Pickaxe")[0]
                returnText += getItemInfo("Jackhammer")[0]
                buy = "/btc buy "
                keyboardLayout.append([buy + "Q-Tip 1"])
                keyboardLayout.append([buy + "Toothpick 1"])
                keyboardLayout.append([buy + "Chisel 1"])
                keyboardLayout.append([buy + "Pickaxe 1"])
                keyboardLayout.append([buy + "Jackhammer 1"])
                keyboardLayout.append(["/btc exit"])
            elif newCommand[1] == "consumables":
                returnText = "Consumables! Page 1:\n"
                returnText += getItemInfo("Steroid")[0]
                buy = "/btc buy "
                keyboardLayout.append([buy + "Steroid"])
                keyboardLayout.append(["/btc exit"])
            elif newCommand[1] == "stocks":
                returnText = getPortfolio(True)
                prefix = "/btc stock "
                keyboardLayout.append([prefix + "A"])
                keyboardLayout.append([prefix + "B"])
                keyboardLayout.append([prefix + "C"])
                keyboardLayout.append([prefix + "D"])
                keyboardLayout.append([prefix + "S"])
                keyboardLayout.append(["/btc exit"])
            elif newCommand[1] == "weapons":
                returnText = "Out to deal some damage, eh?\n"
                returnText += getItemInfo("Hammer")[0] + "\n"
                returnText += getItemInfo("Crowbar")[0]
                prefix = "/btc buy "
                keyboardLayout.append([prefix + "Hammer"])
                keyboardLayout.append([prefix + "Crowbar"])
                keyboardLayout.append(["/btc exit"])
            else:
                returnText = "Sorry! Not implemented yet."
                returnMessageType = ""
        return [returnText, returnMessageType, keyboardLayout]

    def stock(newCommand):
        user = getUser(currentMessage.from_user.id)
        if len(newCommand) > 1: #managing stock
            if len(newCommand) > 2: #actual buy or sell command has been sent
                stock = getStockBySymbol(newCommand[1])
                if newCommand[2] == "buy" and stock != None:
                    print("We're buying!")
                    quantityPurchased = 1
                    try:
                        quantityPurchased = int(newCommand[-1])
                    except:
                        pass
                    if quantityPurchased < 0:
                        quantityPurchased *= -1
                    if stock['currentValue'] * quantityPurchased > float(user['money']):
                        quantityPurchased = int(float(user['money'])/stock['currentValue'])
                    if float(user['money']) < stock['currentValue'] * quantityPurchased or quantityPurchased == 0: #can't afford
                        return ["I'm afraid you can't afford that.", ""]
                    builtins.btcDB.update(user, money=user['money'] - (stock['currentValue'] * quantityPurchased))
                    portfolio = user['stocks']
                    portfolio[stock['letter']] += quantityPurchased
                    builtins.btcDB.update(user, stocks=portfolio)
                    builtins.btcDB.commit()
                    return ["You bought " + str(quantityPurchased) + " shares of " + stock['name'] + " at " + str(stock['currentValue']) + strBtc + ". You now have " + str(user['stocks'][stock['letter']]) + " shares (" + str(floatRound(stock['currentValue'] * user['stocks'][stock['letter']])) + strBtc + ") in that stock.", ""]
                elif newCommand[2] == "sell" and stock != None:
                    quantitySold = 1
                    try:
                        quantitySold = int(newCommand[-1])
                    except:
                        pass
                    if quantitySold < 0:
                        quantitySold *= -1
                    if quantitySold > user['stocks'][stock['letter']]:
                        quantitySold = user['stocks'][stock['letter']]

                    builtins.btcDB.update(user, money=floatRound(user['money'] + (stock['currentValue'] * quantitySold)))
                    portfolio = user['stocks']
                    portfolio[stock['letter']] -= quantitySold
                    builtins.btcDB.update(user, stocks=portfolio)
                    builtins.btcDB.commit()
                    return ["You sold " + str(quantitySold) + " shares of " + stock['name'] + ", making " + str(floatRound(stock['currentValue'] * quantitySold)) + strBtc + ". You have " + str(user['stocks'][stock['letter']]) + " shares (" + str(floatRound(user['stocks'][stock['letter']] * stock['currentValue'])) + strBtc + ") left.", ""]
                elif newCommand[2] == "history" and stock != None:
                    return [stock['history'][max(0, len(stock['history']) - 24):-1] + [stock['history'][-1]], ""]
                else:
                    return ["Invalid stock symbol.", ""]
            else:
                keyboardLayout = []
                message = "Would you like to buy or sell this stock, or view its history?"
                keyboardLayout.append(["/btc stock " + newCommand[1] + " buy 1"])
                keyboardLayout.append(["/btc stock " + newCommand[1] + " sell 1"])
                keyboardLayout.append(["/btc stock " + newCommand[1] + " history"])
                return [message, "keyboard", keyboardLayout]
        else:
            return ["Go to the shop to start buying stocks.", ""]

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
                if itemInfo[2] != "weapon":
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
                        builtins.btcDB.update(user, money=floatRound(user['money'] - itemInfo[1]))
                        builtins.btcDB.update(user, positiveMultiplier=itemInfo[3])
                        builtins.btcDB.update(user, positiveYields=1)
                        builtins.btcDB.commit()
                        return ["You bought a " + newCommand[1] + ". Your next yield will be multiplied by " + str(itemInfo[3]) + ", making it " + str(floatRound(user['myYield'] * itemInfo[3])) + strBtc + ". You now have " + str(user['money']) + strBtc + ".", ""]
                    else:
                        return ["You already have a consumable active.", ""]
                elif itemInfo[2] == "weapon":
                    isConfirming = False
                    target = ""
                    try:
                        isConfirming = newCommand[3] == "yes"
                    except:
                        pass

                    try:
                        target = newCommand[2]
                    except:
                        pass

                    if target == "":
                        outputString = "\n```\nYou want a " + newCommand[1] + "? Select a target."
                        if itemInfo[4] < 0:
                            outputString += " (Just know, you can't bring anyone's balance below 0" + strBtc + ".)\n"
                        keyboardLayout = []
                        prefix = "/btc buy "
                        keyboardLayout.append(["/btc exit"])
                        K = list()
                        for u in builtins.btcDB:
                            K.append(u)
                        sortedK = sorted(K, key=lambda x: float(x['myYield']), reverse=True)
                        print("Sorted K?")
                        for userA in sortedK:
                            if user['username'] != userA['username']:
                                outputString += userA['username'] + " (" + userA['name'] + ")\n\t" + str(floatRound(userA['money'])) + strBtc + " - " + str(userA['myYield']) + strBtc + strPerHour + ": "
                                outputString += str(floatRound(userA['myYield'] * float(itemInfo[3]))) + strBtc + "\n"
                                keyboardLayout.append([prefix + newCommand[1] + " " + userA['username']])
                        outputString += "```"
                        return [outputString, "keyboard", keyboardLayout]
                    elif target != "yes" and target != "" and not isConfirming:
                        targetUser = getUserByUsername(newCommand[2])
                        if targetUser == None:
                            return ["How are you going to use a weapon on someone who doesn't exist?", ""]
                        cost = floatRound(targetUser['myYield'] * float(itemInfo[3]))
                        outputString = "You want to use a " + newCommand[1] + " on " + newCommand[2] + "?\nThat's going to cost you " + str(cost) + strBtc + ".\nYou sure?"
                        keyboardLayout = []
                        keyboardLayout.append(["/btc buy " + newCommand[1] + " " + newCommand[2] + " yes"])
                        keyboardLayout.append(["/btc exit"])
                        return [outputString, "keyboardnm", keyboardLayout]
                    elif isConfirming:
                        targetUser = getUserByUsername(newCommand[2])
                        cost = floatRound(targetUser['myYield'] * float(itemInfo[3]))
                        effect = itemInfo[4]
                        if targetUser == None:
                            return ["How are you going to use a weapon on someone who doesn't exist?", ""]
                        elif targetUser['username'] == user['username']:
                            return ["Sorry, I'm not going to let you use a weapon on yourself.", ""]
                        elif cost > user['money']:
                            return ["Why are you looking to attack others when you're so poor yourself?", ""]

                        builtins.btcDB.update(user, money=floatRound(user['money'] - cost))
                        if effect == 0:
                            if targetUser['zeroYields'] > 0:
                                return ["They've already had their yield set to 0 this hour.", ""]
                            builtins.btcDB.update(targetUser, zeroYields=1)
                        elif effect <= 0:
                            if targetUser['negativeYields'] > 0:
                                return ["They've already had their yield set negative this hour.", ""]
                            builtins.btcDB.update(targetUser, negativeYields=1)
                            builtins.btcDB.update(targetUser, negativeMultiplier=effect)
                        builtins.btcDB.commit()
                        if int(targetUser['chat_id']) != 0:
                            sendTextTo(user['name'] + " attacked you with a " + newCommand[1] + ", multiplying your next yield by " + str(effect) + ".", int(targetUser['chat_id']))
                        return ["You attacked " + targetUser['name'] + " with a " + newCommand[1] + ".", ""]
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
            defaultStockArray = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
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
            builtins.btcDB.insert(currentMessage.from_user.id, username, name, 1.0, 0.1, 0, 0, -1, 0, 0, 0, 000000, defaultStockArray, {})
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
        elif newCommand[0] == "stock":
            return stock(newCommand)
        elif newCommand[0] == "portfolio":
            return [getPortfolio(), "markdown"]
        elif newCommand[0] == "me":
            return [getMe(), "markdown"]
        elif newCommand[0] == "exit":
            return ["Bye!", ""]
        elif newCommand[0] == "quote":
            return [stockQuote(), "markdown"]
        elif newCommand[0] == "remove":
            builtins.btcDB.delete(getUser(currentMessage.from_user.id))
            return["Sorry to see you go. :(", ""]
        elif currentMessage.from_user.username == "AdamZG":
            if newCommand[0] == "commit":
                builtins.btcDB.commit()
                return ["Committed the BTC database.", ""]
            elif newCommand[0] == "debug":
                print(getUserByUsername("AdamZG")['stocks'])
                return ["Printed the thing?", ""]
            elif newCommand[0] == "migrate":
                defaultStockArray = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
                for user in builtins.btcDB:
                    builtins.btcDB1.insert(user['id'], user['username'], user['name'], user['money'], user['myYield'], user['positiveMultiplier'], user['positiveYields'], user['zeroMultiplier'], user['zeroYields'], user['negativeMultiplier'], user['negativeYields'], user['chat_id'], defaultStockArray, {})
                builtins.btcDB1.commit()
                return ["Migrated.", ""]
            elif newCommand[0] == "resetStocks":
                defaultStockArray = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
                for user in builtins.btcDB:
                    builtins.btcDB.update(user, stocks=defaultStockArray.copy())
                builtins.btcDB.commit()
                return ["reset stocks. economies that exist: not ours", ""]
            elif newCommand[0] == "iS":
                defineStocks()
                return ["We did the stocks", ""]
            elif newCommand[0] == "uS":
                i = 1
                try:
                    i = int(newCommand[-1])
                except:
                    pass
                for a in range(0, i):
                    print(a)
                    updateStocks()
                return ["Updated stocks " + str(i) + " times", ""]
            elif newCommand[0] == "give":
                user = getUserByUsername(newCommand[1])
                builtins.btcDB.update(user, money=user['money'] + int(newCommand[2]))
                sendTextTo("Admin gave you " + newCommand[2] + strBtc, user['chat_id'])
                return ["Wow, cheater.", ""]
            elif newCommand[0] == "updateStockRange":
                return updateStockRange(newCommand[1], float(newCommand[2]), float(newCommand[3]))
            elif newCommand[0] == "updateStockRangeSize":
                return updateStockRangeSize(newCommand[1], float(newCommand[2]))
            elif newCommand[0] == "getStockInfo":
                return getStockInfo(newCommand[-1])

    else:
        print("Not valid private chat command.")
        return ["", "no"]






#('id', 'username', 'name', 'money', 'myYield', 'positiveMultiplier', 'positiveYields', 'zeroMultiplier', 'zeroYields', 'negativeMultiplier', 'negativeYields', 'chat_id')

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

def getQuote(chat_id):
    try:
        with open("chatStorage/" + str(chat_id) + "quoteArray.csv", "r+") as csvfile:
            reader = csv.DictReader(csvfile)
            quoteArrayCurrent = list(reader)
            print(quoteArrayCurrent)
            return random.choice(quoteArrayCurrent)['quote']
    except Exception:
        print(traceback.format_exc())
        return "[undefined]"

def quoteable(chat_id):
    response = ""
    try:
        with open("chatStorage/" + str(chat_id) + "quoteArray.csv", "r+") as csvfile:
            reader = csv.DictReader(csvfile)
            quoteArrayCurrent = list(reader)
            response = "Current list of quotes:\n"
            for x in quoteArrayCurrent:
                response += x['quote'] + "\n"
        return response
    except Exception:
        return "No /quote list defined. Use /quoteadd to add a quote."

def quoteDefine(chat_id, messageText):
    theText = messageText[len("/quotedefine "):]
    wholeTextArray = re.split(r'[,*]', theText)
    fieldnames = ['quote']
    if len(messageText) > len("/quotedefine "):
        with open("chatStorage/" + str(chat_id) + "quoteArray.csv", "w+") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for quote in wholeTextArray:
                writer.writerow({'quote': quote})
        return True
    else:
        with open("chatStorage/" + str(chat_id) + "quoteArray.csv", "w+") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        return False

def quoteAdd(chat_id, messageText):
    try:
        if len(messageText) > len("/quoteadd "):
            messageText = messageText.replace(",","").replace('*', "'")
            with open("chatStorage/" + str(chat_id) + "quoteArray.csv", "r+") as csvfile:
                reader = csv.DictReader(csvfile)
                quoteArrayCurrent = []
                for row in reader:
                    quoteArrayCurrent.append(row['quote'])
                myStr = ", ".join(quoteArrayCurrent)
            return quoteDefine(chat_id, "/quotedefine " + myStr + ", " + messageText.replace("/quoteadd ", ""))
        else:
            return False
    except Exception:
        return quoteDefine(chat_id, messageText.replace("quoteadd ", "quotedefine "))

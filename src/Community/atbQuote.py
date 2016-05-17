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
import pydblite

import telegram

def getQuote(chat_id):
    db = pydblite.Base('chatStorage/quoteDB' + str(chat_id) + '.pdl')
    if not db.exists():
        return "You never added a quote!"
    else:
        db.open()
    entries = list()
    for entry in db:
        entries.append(entry["__id__"])
    recordOfQuote = db[random.choice(entries)]
    if recordOfQuote["addedBy"] == None:
        return "[" + str(recordOfQuote["__id__"]) + "] " + recordOfQuote["quote"] + " - " + recordOfQuote["who"]
    else:
        return "[" + str(recordOfQuote["__id__"]) + "] " + recordOfQuote["quote"] + " - " + recordOfQuote["who"] + " added by " + recordOfQuote["addedBy"]

def getQuoteAt(chat_id, quote_id):
    db = pydblite.Base('chatStorage/quoteDB' + str(chat_id) + '.pdl')
    if not db.exists():
        return "You never added a quote!"
    else:
        db.open()
    try:
        recordOfQuote = db[quote_id]
        if recordOfQuote["addedBy"] == None:
            return "[" + str(recordOfQuote["__id__"]) + "] " + recordOfQuote["quote"] + " - " + recordOfQuote["who"]
        else:
            return "[" + str(recordOfQuote["__id__"]) + "] " + recordOfQuote["quote"] + " - " + recordOfQuote["who"] + " added by " + recordOfQuote["addedBy"]
    except:
        return "Quote not found"

def getQuoteFrom(chat_id, name):
    db = pydblite.Base('chatStorage/quoteDB' + str(chat_id) + '.pdl')
    if not db.exists():
        return "You never added a quote!"
    else:
        db.open()
    entries = list()
    for entry in (db("who") == name):
        entries.append(entry["__id__"])
    if entries == []:
        return "No quotes from this name found"
    else:
        recordOfQuote = db[random.choice(entries)]
    if recordOfQuote["addedBy"] == None:
        return "[" + str(recordOfQuote["__id__"]) + "] " + recordOfQuote["quote"] + " - " + recordOfQuote["who"]
    else:
        return "[" + str(recordOfQuote["__id__"]) + "] " + recordOfQuote["quote"] + " - " + recordOfQuote["who"] + " added by " + recordOfQuote["addedBy"]

def quoteRemove(chat_id, quote_id):
    db = pydblite.Base('chatStorage/quoteDB' + str(chat_id) + '.pdl')
    if not db.exists():
        return False
    else:
        db.open()
    try:
        del db[quote_id]
        db.commit()
        return True
    except:
        return False

def quoteAdd(chat_id, quoteAdd, quoteOf, whoAdded = None):
    try:
        db = pydblite.Base('chatStorage/quoteDB' + str(chat_id) + '.pdl')
        db.create('quote', 'who', 'addedBy', mode="open")
        db.insert(quote=quoteAdd, who=quoteOf, addedBy=whoAdded)
        db.commit()
    except Exception:
        print("quoteadd failed")
        return False

def getQuoteLegacy(chat_id):
    try:
        with open("chatStorage/" + str(chat_id) + "quoteArray.csv", "r+") as csvfile:
            reader = csv.DictReader(csvfile)
            quoteArrayCurrent = list(reader)
            return random.choice(quoteArrayCurrent)['quote']
    except Exception:
        print(traceback.format_exc())
        return "You never used the old quote format"
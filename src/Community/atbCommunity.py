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

from .. import atbSendFunctions
from .. import atbMiscFunctions

#If you make your own python files for processing data, put them
#In the community folder and import them here:


####

chatInstanceArray = {}

def process(bot, chat_id, parsedCommand, messageText, currentMessage, update, instanceAge):
    def sendText(givenText, replyingMessageID=0, keyboardLayout=[]):
        if not chatInstanceArray[chat_id]['adminDisable']:
            atbSendFunctions.sendText(bot, chat_id, givenText, replyingMessageID, keyboardLayout)

    def sendPhoto(imageName):
        atbSendFunctions.sendPhoto(bot, chat_id, "images/"+ imageName)

    def passSpamCheck():
        return atbMiscFunctions.spamCheck(chat_id, currentMessage.date)


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
                for i in range (0, random.randint(3, 75)):
                    response += "O"
                sendText(response + "M")

        elif parsedCommand == "/swag":
            sendText("swiggity swag, what\'ts in the bag?")



        #this command should go last:
    elif parsedCommand == "/community": #add your command to this list
            response = "/mom - get the camera\n"
            response += "/mooom (any number of \'o\'s) - call for help\n"
            response += "/swag - more memes\n"

            sendText("response")

        else:
            return False

        return True
    except Exception:
        print traceback.format_exc()
        return False
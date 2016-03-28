import telegram


def sendText(bot, chat_id, messageText, replyingMessageID=0, keyboardLayout=[], killkeyboard=True, markdown=False):
    bot.sendChatAction(chat_id=chat_id, action='typing')
    for char in messageText:
        try:
            print(char, end='')
        except:
            print("_", end='')
    print(" at " + str(chat_id))
    #try:
    #    print(messageText.encode("utf-8") + " at " + str(chat_id))
    #except Exception:
    #    print("Sent something with weird characters to " + str(chat_id))

    if replyingMessageID != 0:
        bot.sendMessage(chat_id=chat_id, text=messageText, reply_to_message_id=replyingMessageID, reply_markup=telegram.ReplyKeyboardHide(hide_keyboard=killkeyboard))
    elif keyboardLayout != []:
        print("tried sending keyboard")
        if markdown:
            bot.sendMessage(chat_id=chat_id, text=messageText, parse_mode="Markdown", reply_markup=telegram.ReplyKeyboardMarkup(keyboard=keyboardLayout, one_time_keyboard=True, resize_keyboard=True))
        else:
            bot.sendMessage(chat_id=chat_id, text=messageText, reply_markup=telegram.ReplyKeyboardMarkup(keyboard=keyboardLayout, one_time_keyboard=True, resize_keyboard=True))
    else:
        if markdown:
            bot.sendMessage(chat_id=chat_id, text=messageText, parse_mode="Markdown", reply_markup=telegram.ReplyKeyboardHide(hide_keyboard=killkeyboard))
        else:
            bot.sendMessage(chat_id=chat_id, text=messageText, reply_markup=telegram.ReplyKeyboardHide(hide_keyboard=killkeyboard))

def sendPhoto(bot, chat_id, imagePath):
    bot.sendChatAction(chat_id=chat_id, action='upload_photo')
    print("Sending picture to " + str(chat_id))
    bot.sendPhoto(chat_id=chat_id, photo=open(imagePath, "rb"))

def sendSticker(bot, chat_id, sticker):
    bot.sendChatAction(chat_id=chat_id, action='typing')
    print("Sending sticker to " + str(chat_id))
    bot.sendSticker(chat_id=chat_id, sticker=open(sticker, "rb"))

def sendVideo(bot, chat_id, videoPath):
    bot.sendChatAction(chat_id=chat_id, action='upload_video')
    print("Sending video to " + str(chat_id))
    bot.sendVideo(chat_id=chat_id, video=open(videoPath, "rb"))
def sendAudio(bot, chat_id, audioPath):
    bot.sendChatAction(chat_id=chat_id, action='upload_audio')
    print("Sending audio to " + str(chat_id))
    bot.sendAudio(chat_id=chat_id, audio=open(audioPath, "rb"))

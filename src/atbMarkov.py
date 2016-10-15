import telegram
import markovify
import builtins
import re
import traceback


def processTextOld(text):
    if builtins.markov == None:
        print("Setting to text")
        builtins.markov = markovify.Text(text)
    else:
        print("Combining")
        builtins.markov = markovify.combine([builtins.markov, markovify.Text(text)], [0.5, 0.5])

def processText(text):
    text.replace(".", "\n", 999)
    text
    f = open('chatStorage/markov.txt', mode='a')
    f.write('\n\n')
    f.write(text)
    f.close()

    

def getMarkov(messageText):
    #if markov is None, just return "not enough info"

    f = open('chatStorage/markov.txt', mode='r')
    myText = ""
    for line in f:
        myText += line + "\n"

    builtins.markov = markovify.NewlineText(myText)
    ret = ""

    lastWord = re.split(r'[@\s:,\'*]', messageText.lower())[-1]
    if lastWord.lower() != "/markov" and lastWord in myText:
        try:
            ret = builtins.markov.make_sentence_with_start(lastWord, tries=50)
        except Exception:
            print(traceback.format_exc())
            ret = ""
    
    if ret == "":
        ret = builtins.markov.make_short_sentence(140, tries=30)

    
    if ret == "" or ret == None:
        x = random.randint(0, 5)
        if x == 0:
            ret = "haha"
        elif x == 1:
            ret = "good, good"
        elif x == 2:
            ret = "Don't you have someone else to be bothering?"
        elif x == 3:
            ret = "nah"
        elif x == 4:
            ret = "lmao"
        elif x == 5:
            ret = "shhhhhhhhhhh"
    
    return ret.capitalize()

    
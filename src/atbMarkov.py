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

    #if messageText is just command
    if len(re.split(r'[@\s:,\'*]', messageText)) == 1:
        try:
            ret = builtins.markov.make_short_sentence(140, tries=30)
        except Exception as e:
            print(traceback.format_exc())
            ret = ""
    else:
        #use last word in sentence as sentence starter
        lastWord = re.split(r'[@\s:,\'*]', messageText.lower())[-1]
        try:
            ret = builtins.markov.make_sentence_with_start(lastWord, tries=50)
        except Exception:
            print(traceback.format_exc())
            try:
                ret = builtins.markov.make_short_sentence(140, tries=30)
            except:
                print(traceback.format_exc())
                ret = ""

    
    if ret == "" or ret == None:
        ret = "Issue with Markov chaining."
    
    return ret.capitalize()

    
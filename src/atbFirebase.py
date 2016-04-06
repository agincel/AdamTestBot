from firebase import firebase
import builtins #I'm so sorry

def update():
    fb = firebase.FirebaseApplication("https://adamtestbotstats.firebaseio.com", None)
    blazeDb = []
    btcLedger = []
    stocks = []
    for user in builtins.blazeDB:
        scoreStr = ""
        if user['topThree']:
            scoreStr += "+ "
        if user['streak'] > 1:
            scoreStr += "(" + str(user['streak']) + ") "
        blazeDb.append([user['name'], scoreStr + str(user['score'])])
    for user in builtins.btcDB:
        yieldStr = ""
        if user['positiveYields'] > 0:
            yieldStr += "(" + str(user['positiveMultiplier']) + "x) "
        if user['negativeYields'] > 0:
            yieldStr += "(" + str(user['negativeMultiplier']) + "x) "
        if user['zeroYields'] > 0:
            yieldStr += "(0x) "
        yieldStr += str(user['myYield'])
        btcLedger.append([user['name'], round(user['money'], 3), yieldStr])
    for stock in builtins.btcStockDB:
        stocks.append([stock['name'], stock['currentValue']])
    allInfo = {'blazeDb': blazeDb, 'btcLedger': btcLedger, 'stocks': stocks}
    fb.delete("/stats", None)
    fb.post("/stats", allInfo)
    print("Updated website.")


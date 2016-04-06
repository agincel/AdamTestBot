from firebase import firebase
import builtins #I'm so sorry

def update():
    fb = firebase.FirebaseApplication("https://adamtestbotstats.firebaseio.com", None)
    blazeDb = []
    btcLedger = []
    stocks = []
    K = list()
    for user in builtins.blazeDB:
        K.append(user)
    sortedK = sorted(K, key=lambda x: int(x['score']), reverse=True)
    for user in sortedK:
        scoreStr = ""
        if user['topThree']:
            scoreStr += "+ "
        if user['streak'] > 1:
            scoreStr += "(" + str(user['streak']) + ") "
        blazeDb.append([scoreStr + user['name'], user['score']])
    K = list()
    for user in builtins.btcDB:
        K.append(user)
    sortedK = sorted(K, key=lambda x: float(x['myYield']), reverse=True)
    for user in sortedK:
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


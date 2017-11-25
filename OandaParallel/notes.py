

def printMethod():

    bodyContent = json.loads(body.getvalue())
    pprint.pprint(bodyContent)
    print(json.dumps(bodyContent, indent=1))





parametersDict['rcRatioClose'] =np.arange(0.01, 0.35, 0.03)
parametersDict['rcRatioOpen'] =          np.arange(0.01, 0.35, 0.03)      
parametersDict['rcRatioCloseDirection'] = [0.42]
parametersDict['rcRatioOpenDirection'] = [0.58]
parametersDict['atrRatio'] = [1.22]
parametersDict['RSIOversold'] = [30]
parametersDict['RSIOverbought'] =[70]
parametersDict['StochRSIOversold'] =[12]
parametersDict['StochRSIOverbought'] =[88]
parametersDict['RSIOversoldClose'] =[30]
parametersDict['RSIOverboughtClose'] =[70]
parametersDict['StochRSIOversoldClose'] =[10]
parametersDict['StochRSIOverboughtClose'] =[90]
parametersDict['stopLossRatio'] =[0.002]
parametersDict['takeProfitRatio'] =[0.05]
parametersDict['trailingStopRatio'] =[0.0075]
parametersDict['deviationRatioBelow'] =[0.0055],
parametersDict['deviationRatioAbove'] = [0.0015], 
parametersDict['candleRange'] =[1.05],
parametersDict['rangeOverDeviationBelow'] = [10],
parametersDict['rangeOverDeviationAbove'] =  [0],
parametersDict['ADXLevelBelow'] = [35]   


parametersList = list(parametersDict.values())
    

def indicatorSignals(data, RSIB, RSIS, STOCHB, STOCHS): 

    data = data.assign(Overbought = ((data.loc[:, 'RSI7'] > RSIB) & (data.loc[:, 'StochRSI_K14/3'] > STOCHB)))
    data = data.assign(Oversold = ((data.loc[:, 'RSI7'] < RSIS) & (data.loc[:, 'StochRSI_K14/3'] < STOCHS)))
    return data


def userInput():
    endpoints = ['account', 'instrument', 'order', 'trade', 'position', 'transaction', 'princing', 'forex labs']
    endpoint = input("enter asdfsda fa f") 


#userInput()


def RSICust(data, period):


    data['gainLoss'] = data['c'].diff()

    data['gain'] = np.where(data['gainLoss'] > 0, data['gainLoss'], 0)
    data['loss'] = np.where(data['gainLoss'] < 0, data['gainLoss'].abs(), 0)

    data['avgGain'] = data['gain'].ewm(adjust = False, alpha = (1/period), min_periods= 1).mean()
    data['avgLoss'] = data['loss'].ewm(adjust = False, alpha = (1/period), min_periods= 1).mean()

    data = data.assign(RS = data["avgGain"] / data["avgLoss"])
    data = data.assign(RSI= 100 - (100 / (1 + data['RS'])))
    data = data.rename(columns={'RSI': 'RSI' + str(period)})

    #--------------------for loop for the EMA - starts with the sma--------------------#
 
    #data["avgGain"] = np.nan
    #data["avgLoss"] = np.nan
    #data.loc[7, "avgGain"] = (data['gain'][1:8]).mean()
    #data.loc[7, "avgLoss"] = (data['loss'][1:8]).mean()

    #for i in range(len(data["avgGain"][8:])):
    #    data.loc[(i + 8), 'avgGain'] = (data.loc[(i + 7), 'avgGain'] * 6 + data.loc[(i + 8), 'gain']) / 7


    #for i in range(len(data["avgLoss"][8:])):
    #    data.loc[(i + 8), 'avgLoss'] = (data.loc[(i + 7), 'avgLoss'] * 6 + data.loc[(i + 8), 'loss']) / 7


    #--------------------for loop for the EMA - starts with the sma--------------------#      

    #data["avgGain"] = pd.Series.rolling(data['gain'], window = 7 ).mean()
    #data["avgLoss"] = pd.Series.rolling(data['loss'], window = 7 ).mean()

    return data

def RSICustII(data, period):


    data['gainLoss'] = data['c'].diff()

    data['gain'] = np.where(data['gainLoss'] > 0, data['gainLoss'], 0)
    data['loss'] = np.where(data['gainLoss'] < 0, data['gainLoss'].abs(), 0)


    #--------------------for loop for the EMA - starts with the sma--------------------#
 
    data["avgGain"] = np.nan
    data["avgLoss"] = np.nan
    data.loc[7, "avgGain"] = (data['gain'][1:8]).mean()
    data.loc[7, "avgLoss"] = (data['loss'][1:8]).mean()

    for i in range(len(data["avgGain"][8:])):
        data.loc[(i + 8), 'avgGain'] = (data.loc[(i + 7), 'avgGain'] * 6 + data.loc[(i + 8), 'gain']) / 7


    for i in range(len(data["avgLoss"][8:])):
        data.loc[(i + 8), 'avgLoss'] = (data.loc[(i + 7), 'avgLoss'] * 6 + data.loc[(i + 8), 'loss']) / 7


    #--------------------for loop for the EMA - starts with the sma--------------------#   


    data = data.assign(RS = data["avgGain"] / data["avgLoss"])
    data = data.assign(RSI= 100 - (100 / (1 + data['RS'])))
    data = data.rename(columns={'RSI': 'RSI' + str(period)})

    #data["avgGain"] = pd.Series.rolling(data['gain'], window = 7 ).mean()
    #data["avgLoss"] = pd.Series.rolling(data['loss'], window = 7 ).mean()

    return data

def RSICustIII(data, period):


    data['gainLoss'] = data['c'].diff()

    data['gain'] = np.where(data['gainLoss'] > 0, data['gainLoss'], 0)
    data['loss'] = np.where(data['gainLoss'] < 0, data['gainLoss'].abs(), 0)

    sma = pd.Series(np.nan)   #.rolling(data['gain'], window = 7, min_periods = 7 ).mean()[:7]

    sma[7] = (data['gain'][1:8]).mean()
    rest = data['gain'][8:]

    data["avgGain"] = pd.concat([sma, rest]).ewm(adjust = False, alpha = (1/7)).mean()
    print(data["avgGain"])

    #--------------------for loop for the EMA - starts with the sma--------------------#
 
    #data["avgGain"] = np.nan
    #data["avgLoss"] = np.nan
    #data.loc[7, "avgGain"] = (data['gain'][1:8]).mean()
    #data.loc[7, "avgLoss"] = (data['loss'][1:8]).mean()

    #for i in range(len(data["avgGain"][8:])):
    #    data.loc[(i + 8), 'avgGain'] = (data.loc[(i + 7), 'avgGain'] * 6 + data.loc[(i + 8), 'gain']) / 7


    #for i in range(len(data["avgLoss"][8:])):
    #    data.loc[(i + 8), 'avgLoss'] = (data.loc[(i + 7), 'avgLoss'] * 6 + data.loc[(i + 8), 'loss']) / 7


    #--------------------for loop for the EMA - starts with the sma--------------------#      


    #data = data.assign(RS = data["avgGain"] / data["avgLoss"])
    #data = data.assign(RSI= 100 - (100 / (1 + data['RS'])))
    #data = data.rename(columns={'RSI': 'RSI' + str(period)})

    #data["avgGain"] = pd.Series.rolling(data['gain'], window = 7 ).mean()
    #data["avgLoss"] = pd.Series.rolling(data['loss'], window = 7 ).mean()

    return data

def bearishRejectionCandle(row, ratio):

    try:

        if 0.001 < (row['c'] - row['l']) / (row['h'] - row['l']) < ratio:
            return True
        else:
            return False

    except ZeroDivisionError:
        return False

def bullishRejectionCandle(row, ratio):

    try:
        
        if 0.001 < ((row['c'] - row['h']) / (row['l'] - row['h']))  < ratio:
            return True
        else:
            return False

    except ZeroDivisionError:
        return False

def bearishRejectionCandle(data, ratio):

    
    data = data.assign(high_low = np.where(((data['h'] - data['l']) != 0), (data['h'] - data['l']), np.NaN))
    data = data.assign(BearishRejectionCandle =   (((data['c']  - data['l']) / (data['h'] - data['l']) < ratio)) & 
                                                   ((data['c']  - data['l']) / (data['h'] - data['l']) > 0.001))


    return data


def bullishRejectionCandle(data, ratio):

    
    data = data.assign(high_low = np.where(((data['l'] - data['h']) != 0), (data['l'] - data['h']), np.NaN))
    data = data.assign(BullishRejectionCandle =   (((data['c']  - data['h']) / (data['l'] - data['h']) < ratio)) & 
                                                   ((data['c']  - data['h']) / (data['l'] - data['h']) > 0.001))


    return data


#print(re.match(r'StochRSI_D(..?..)', 'StochRSI_D14/3').group(0))
#print('StochRSI_D(..?..)' in 'StochRSI_D14/3')
#print('StochRSI' in 'StochRSI_D14/3')
#print('StochRSI' in list(data.columns.values))



#python -m cProfile -o program.prof backtestControl.py
#snakeviz program.prof








def rollingSlope(data):
     
        
    y = pd.Series(range(len(data)))
    X = pd.Series(data)
    X = sm.add_constant(X)
    res = sm.OLS(y, X).fit()

    return res.params[1]

def rollingCorrelation(data):
     
        
    y = pd.Series(range(len(data)))
    X = pd.Series(data)
    X = sm.add_constant(X)
    res = sm.OLS(y, X).fit()

    return math.sqrt(res.rsquared)


    
    
data['RegressionSlope' + str(period)]           = data['c'].rolling(window = 10).apply(rollingSlope)
data['RegressionCorrelation' + str(period)]     = data['c'].rolling(window = 10).apply(rollingCorrelation)

import pprint
import pandas as pd
import numpy as np
import main
import time
import datetime
import itertools
import pickle
import _pickle as pk
import dateList
import backtest
import marshal
import os




#-----data------#
startDate = datetime.datetime(2007, 1, 1, 0, 0, 0)
endDate = datetime.datetime(2017, 1, 1, 0, 0, 0)
interval = 'H2'
offset = None


if interval == 'M15':
    dateList = dateList.make15Minutes(startDate, endDate)
    offset = 15
elif interval == 'H1':
    dateList = dateList.make1Hour(startDate, endDate)
    offset = 60
elif interval == 'H2':
    dateList = dateList.make1Hour(startDate, endDate)
    offset = 120
elif interval == 'H4':
    dateList = dateList.make1Hour(startDate, endDate)
    offset = 240
elif interval == 'D':
    dateList = dateList.makeDays(startDate, endDate)
    offset = 1440


def getData(startDate, endDate):

    t0 = time.clock()

    data_Object = main.dataObject()


    #dataDict = data_Object.dataBuild(interval, startDate, endDate, offset, \
    #'NZD_CAD')

    #dataDict = data_Object.dataBuild(interval, startDate, endDate, offset, \
    #'AUD_NZD', 'EUR_GBP','CAD_CHF', 'EUR_AUD', 'GBP_AUD', 'AUD_USD',
    #'CAD_CHF', 'EUR_CAD', 'EUR_USD', 'GBP_USD', 'USD_CAD',
    #'USD_JPY', 'USD_MXN', 'NZD_CAD', 'GBP_JPY')

    #dataDict = data_Object.dataBuild(interval, startDate, endDate, offset, \
    #'USD_CAD', 'AUD_CAD', 'CAD_CHF', 'EUR_CAD', 'GBP_CAD', 'NZD_CAD', 'CAD_JPY', 'AUD_USD', 'EUR_USD',  \
    #'GBP_USD', 'NZD_USD', 'USD_CHF', 'USD_NOK', 'USD_SEK', 'AUD_CHF', 'AUD_NZD', 'EUR_AUD', 'EUR_CHF',  \
    #'EUR_GBP', 'EUR_NOK', 'EUR_NZD', 'EUR_SEK', 'GBP_AUD', 'GBP_CHF', 'GBP_NZD', 'NZD_CHF', 'USD_JPY',  \
    #'AUD_JPY', 'CHF_JPY', 'EUR_JPY', 'GBP_JPY' ,'NZD_JPY', 'USD_MXN')
                                                                                             
         



    #pickle.dump(dataDict, open('dataSave\\' + '2hoursChannel', 'wb'))
    #dataDict = pickle.load(open( 'dataSave\\' + '2hoursChannel', 'rb'))
    #dataDict = pickle.load(open('OandaParallel' + '\\dataSave\\' + '2hoursChannelSeries', 'rb'))
    dataDict = pickle.load(open('dataSave\\' + '2hoursChannelSeries', 'rb'))
    #dataDict = pickle.load(open( 'dataSave\\' + '2hoursChannelSeriesAll', 'rb'))
    #dataDict = pickle.load(open('dataSave\\' + '4hoursChannelSeries', 'rb'))
    #pprint.pprint(dataDict)


    global seriesAlreadySet
    seriesAlreadySet = True


    t1 = time.clock()
    print('Get data time: ', t1 - t0) 

    

    return data_Object, dataDict 


data_Object, dataDict = getData(startDate, endDate)
data = dataDict.copy()


def setParameters(data):
    
    t0 = time.clock()

    for instrument in data.keys():
     
        if interval == 'D':

            data[instrument].index = pd.DatetimeIndex(data[instrument].index).normalize()
                         
        data[instrument] = data_Object.setIndicators(data[instrument],

        ('RSI', 7), 
        ('RSI', 12),
        ('StochRSI', 10, 3, 3), 
        ('StochRSI', 14, 3, 3), 
        ('StochRSI', 20, 3, 3), 
        ('EMA', 'Price', 10), 
        ('EMA', 'Price', 20), 
        ('EMA', 'Price', 50), 
        ('EMA', 'Price', 200),
        ('EMA', 'Price', 365), 
        ('EMA', 'Volume', 5), 
        ('EMA', 'Volume', 10), 
        ('EMA', 'Volume', 20),
        ('BearishRC',),
        ('BullishRC',),
        ('Highest Price', 1),
        ('Lowest Price', 1), 
        ('Highest Price', 2),
        ('Lowest Price', 2), 
        ('Highest Price', 3),
        ('Lowest Price', 3), 
        ('Highest Price', 5),
        ('Lowest Price', 5), 
        ('Highest Price', 10),
        ('Lowest Price', 10), 
        ('ADX', 10),
        ('ADX', 14),
        ('Regression', 20, 1),
        ('Deviation', 10),
        ('Deviation', 20),
        ('Deviation', 100), 
        ('Bollinger Bands', 20, 2.5))



        data[instrument] = data[instrument][np.isfinite(data[instrument]['PriceEMA365'])]
        #pickle.dump(data, open('dataSave\\' + '2hoursChannelWithParameters',
        #'wb' ))
        #data[instrument].to_excel('dataSave\\' + str(instrument) + '.xlsx')
        #print(data[instrument]['2010-08-04 00:00:00': '2010-08-05 00:00:00'])

    t1 = time.clock()
    print('Set parameters time: ', t1 - t0) 

    return data


if seriesAlreadySet == False:

    data = setParameters(data)



    #itemsSet = [(date, instrument) for date in dateList for instrument in
    #data.keys() if date in data[instrument].index]

    t0 = time.clock()
        
    dataDictSeries = {}
    for date in dateList:
        for instrument in data.keys():
            if date in data[instrument].index:
                dataDictSeries[(date, instrument)] = pd.Series.to_dict(data[instrument].ix[date])

    t1 = time.clock()
    print('Set series time: ', t1 - t0) 


    data = dataDictSeries.copy()
    #pickle.dump(data, open('dataSave\\' + '2hoursChannelSeries', 'wb'))


#pickle.dump(data, open('dataSave\\' + '2hoursWorking', 'wb' ))
#parametersFile = open('dataSave\\' + 'transactiondata.txt', "w")


#-----data------#




conditionsSet = [5, 6]





parametersDict = {
'rcRatioClose':             [0.30],
'rcRatioOpen':              [0.40],
'rcRatioCloseDirection':    [0.35],
'rcRatioOpenDirection':     [0.50],
'atrRatio':                 [0.95],
'RSIOversold':              [30],
'RSIOverbought':            [70],
'StochRSIOversold':         [10],
'StochRSIOverbought':       [90],
'RSIOversoldClose':         [20],
'RSIOverboughtClose':       [80],
'StochRSIOversoldClose':    [7],
'StochRSIOverboughtClose':  [93],
'stopLossRatio':            [0.002],
'takeProfitRatio':          [0.0125],
'trailingStopRatio':        [0.0125],
'deviationRatioBelow':      [0.002],
'deviationRatioAbove':      [0.0015],
'ADXLevelBelow':            [55],
'ADXLevelAbove':            [20],

'channelStopLossRatio':            [0.0025],
'channelTakeProfitRatio':          [0.004],
'channelTrailingStopRatio':        [0.003],
'channelDeviationRatioBelow':      [0.001],
'channelDeviationRatioAbove':      [0.0005], 
'channelRollingCorrelation':       [0.90],
'channelTrailingDeviation':        [1.0], 
'channelPeriod':                   [20],

'EMADILevelAbove':             [0],
'EMAdeviationRatioBelow':      [0.020],
'EMAdeviationRatioAbove':      [0.000],
'EMAatrRatio':                 [0.5],
'EMArcRatioClose':             [0.30],
'EMArcRatioOpen':              [0.40],
'EMArcRatioCloseDirection':    [0.30],
'EMArcRatioOpenDirection':     [0.60],
'EMAstopLossRatio':            [0.1],
'EMAtrailingStopLossRatio':    [0.30],
'EMAtakeProfitRatio':          [0.1]
}





bestCombinationMean = {}
bestCombinationMeanPercent = {}
bestCombinationBalance = {}
bestCombinationMeanbyYear = {}
bestCombinationMeanPercentbyYear = {}
bestCombinationBalancebyYear = {}
bestCombinationMeanbyCurrency = {}
bestCombinationMeanPercentbyCurrency = {}
bestCombinationBalancebyCurrency = {}
allPositive = {}
allPositiveBalance = 0
allPositivebyYear = {}

maxMeanReturn = float("-inf")
maxMeanReturnPercent = float("-inf")
maxEndingBalance = float("-inf")


numberOfIterations = 0


firstIteration = True
if firstIteration == True:
    iterations = list(parametersDict.values())
    numberOfIterations = len(list(itertools.product(*iterations)))
    numberOfIterationsRemaining = numberOfIterations
    firstIteration = False




t4 = time.clock()



for parametersDict['rcRatioClose'],                 \
    parametersDict['rcRatioOpen'],                  \
    parametersDict['rcRatioCloseDirection'],        \
    parametersDict['rcRatioOpenDirection'],         \
    parametersDict['atrRatio'],                     \
    parametersDict['RSIOversold'],                  \
    parametersDict['RSIOverbought'],                \
    parametersDict['StochRSIOversold'],             \
    parametersDict['StochRSIOverbought'],           \
    parametersDict['RSIOversoldClose'],             \
    parametersDict['RSIOverboughtClose'],           \
    parametersDict['StochRSIOversoldClose'],        \
    parametersDict['StochRSIOverboughtClose'],      \
    parametersDict['stopLossRatio'],                \
    parametersDict['takeProfitRatio'],              \
    parametersDict['trailingStopRatio'],            \
    parametersDict['deviationRatioBelow'],          \
    parametersDict['deviationRatioAbove'],          \
    parametersDict['ADXLevelBelow'],                \
    parametersDict['ADXLevelAbove'],                \
    parametersDict['channelStopLossRatio'],         \
    parametersDict['channelTakeProfitRatio'],       \
    parametersDict['channelTrailingStopRatio'],     \
    parametersDict['channelDeviationRatioBelow'],   \
    parametersDict['channelDeviationRatioAbove'],   \
    parametersDict['channelRollingCorrelation'],    \
    parametersDict['channelTrailingDeviation'],     \
    parametersDict['channelPeriod'],                \
    parametersDict['EMADILevelAbove'],              \
    parametersDict['EMAdeviationRatioBelow'],       \
    parametersDict['EMAdeviationRatioAbove'],       \
    parametersDict['EMAatrRatio'],                  \
    parametersDict['EMArcRatioClose'],              \
    parametersDict['EMArcRatioOpen'],               \
    parametersDict['EMArcRatioCloseDirection'],     \
    parametersDict['EMArcRatioOpenDirection'],      \
    parametersDict['EMAstopLossRatio'],             \
    parametersDict['EMAtrailingStopLossRatio'],     \
    parametersDict['EMAtakeProfitRatio'],           \
                                \
                                \
                                \
    in list(itertools.product(*list(parametersDict.values()))):    
 
    
        

    #----main objects initializing-----#
    currentPortfolio = backtest.portfolio(10000)
    currentBacktest = backtest.backtest(currentPortfolio)                            
    currentBacktestRecord = backtest.backtestRecord(currentBacktest)       
    #----main objects initializing-----#

    
         
    def setBacktestParameters(currentBacktest):

        currentBacktest.backtestRecord              = currentBacktestRecord
        currentBacktest.dateList                    = dateList
        currentBacktest.conditionsSet               = conditionsSet
        currentBacktest.stopLossRatio               = parametersDict['stopLossRatio']
        currentBacktest.takeProfitRatio             = parametersDict['takeProfitRatio']
        currentBacktest.trailingStopRatio           = parametersDict['trailingStopRatio']
        currentBacktest.rcRatioClose                = parametersDict['rcRatioClose']
        currentBacktest.rcRatioOpen                 = parametersDict['rcRatioOpen']
        currentBacktest.rcRatioCloseDirection       = parametersDict['rcRatioCloseDirection']
        currentBacktest.rcRatioOpenDirection        = parametersDict['rcRatioOpenDirection']
        currentBacktest.atrRatio                    = parametersDict['atrRatio']
        currentBacktest.ADXLevelBelow               = parametersDict['ADXLevelBelow']
        currentBacktest.ADXLevelAbove               = parametersDict['ADXLevelAbove']

        currentBacktest.deviationRatioBelow         = parametersDict['deviationRatioBelow']
        currentBacktest.deviationRatioAbove         = parametersDict['deviationRatioAbove']
        currentBacktest.RSIOversold                 = parametersDict['RSIOversold']
        currentBacktest.RSIOverbought               = parametersDict['RSIOverbought']
        currentBacktest.RSIOversoldClose            = parametersDict['RSIOversoldClose']
        currentBacktest.RSIOverboughtClose          = parametersDict['RSIOverboughtClose']
        currentBacktest.StochRSIOversold            = parametersDict['StochRSIOversold']
        currentBacktest.StochRSIOverbought          = parametersDict['StochRSIOverbought']
        currentBacktest.StochRSIOversoldClose       = parametersDict['StochRSIOversoldClose']
        currentBacktest.StochRSIOverboughtClose     = parametersDict['StochRSIOverboughtClose']

        currentBacktest.channelDeviationRatioBelow  = parametersDict['channelDeviationRatioBelow']
        currentBacktest.channelDeviationRatioAbove  = parametersDict['channelDeviationRatioAbove']
        currentBacktest.channelRollingCorrelation   = parametersDict['channelRollingCorrelation']
        currentBacktest.channelPeriod               = parametersDict['channelPeriod']
        currentBacktest.channelStopLossRatio        = parametersDict['channelStopLossRatio']
        currentBacktest.channelTakeProfitRatio      = parametersDict['channelTakeProfitRatio']
        currentBacktest.channelTrailingStopRatio    = parametersDict['channelTrailingStopRatio']
        currentBacktest.channelTrailingDeviation    = parametersDict['channelTrailingDeviation']

        currentBacktest.EMADILevelAbove             = parametersDict['EMADILevelAbove']
        currentBacktest.EMAdeviationRatioBelow      = parametersDict['EMAdeviationRatioBelow']
        currentBacktest.EMAdeviationRatioAbove      = parametersDict['EMAdeviationRatioAbove']
        currentBacktest.EMAatrRatio                 = parametersDict['EMAatrRatio']
        currentBacktest.EMArcRatioClose             = parametersDict['EMArcRatioClose']
        currentBacktest.EMArcRatioOpen              = parametersDict['EMArcRatioOpen']
        currentBacktest.EMArcRatioCloseDirection    = parametersDict['EMArcRatioCloseDirection']
        currentBacktest.EMArcRatioOpenDirection     = parametersDict['EMArcRatioOpenDirection']
        currentBacktest.EMAstopLossRatio            = parametersDict['EMAstopLossRatio']
        currentBacktest.EMAtrailingStopLossRatio    = parametersDict['EMAtrailingStopLossRatio']
        currentBacktest.EMAtakeProfitRatio          = parametersDict['EMAtakeProfitRatio']



        if interval == 'M15':
            currentBacktest.interval = 0.25
        elif interval == 'H1':
            currentBacktest.interval = 1
        elif interval == 'H2':
            currentBacktest.interval = 2
        elif interval == 'H4':
            currentBacktest.interval = 4
        elif interval == 'D':
            currentBacktest.interval = 24



        return currentBacktest

    currentBacktest = setBacktestParameters(currentBacktest)
    

    #-----execute------#
    currentBacktest.data = data
    t2 = time.clock()
    currentBacktest.execute()
    t3 = time.clock() 
    #-----execute------#




    #-----shutdown per parameters set-----#
    def shutDownParametersSet():

        currentBacktestRecord.updateStats()      

    #-----printStuff per parameters set-----#
        pprint.pprint(currentBacktestRecord.log, indent = 1)
        #pprint.pprint(currentBacktestRecord.instrumentLog, indent = 1)
        #print("{" + "\n".join("{}: {}".format(k, v) for k, v in currentBacktestRecord.logStats.items()) + "}")
        print("{" + "\n".join("{}: {}".format(k, v) for k, v in currentBacktestRecord.logStatsNoTransactions.items()) + "}")     
        #pprint.pprint(currentBacktestRecord.log, parametersFile)
        pprint.pprint(currentBacktestRecord.transactionPLbyYear, indent = 1)
        
        
    shutDownParametersSet()


 
    #-----shutdown per backtest------#


    if currentBacktestRecord.transactionPLArray .size > 20:

        if  np.mean(currentBacktestRecord.transactionPLArray) > maxMeanReturn:
            maxMeanReturn = np.mean(currentBacktestRecord.transactionPLArray)
            bestCombinationMean = currentBacktestRecord.logStatsNoTransactions
            bestCombinationMeanbyYear = currentBacktestRecord.transactionPLbyYear
            bestCombinationMeanbyCurrency = currentBacktestRecord.transactionPLbyCurrency

        if  np.mean(currentBacktestRecord.transactionPL100Array) > maxMeanReturnPercent:
            maxMeanReturnPercent = np.mean(currentBacktestRecord.transactionPL100Array)
            bestCombinationMeanPercent = currentBacktestRecord.logStatsNoTransactions
            bestCombinationMeanPercentbyYear = currentBacktestRecord.transactionPLbyYear
            bestCombinationMeanPercentbyCurrency = currentBacktestRecord.transactionPLbyCurrency

        if  currentBacktest.portfolio.balance > maxEndingBalance:
            maxEndingBalance = currentBacktest.portfolio.balance
            bestCombinationBalance = currentBacktestRecord.logStatsNoTransactions
            bestCombinationBalancebyYear = currentBacktestRecord.transactionPLbyYear
            bestCombinationBalancebyCurrency = currentBacktestRecord.transactionPLbyCurrency


        if all(value > 0 for value in currentBacktestRecord.transactionPLbyYear.values()):
            if not allPositive:
                allPositive = currentBacktestRecord.logStatsNoTransactions
                allPositivebyYear = currentBacktestRecord.transactionPLbyYear
            elif currentBacktest.portfolio.balance > allPositiveBalance:
                allPositiveBalance = currentBacktest.portfolio.balance
                allPositive = currentBacktestRecord.logStatsNoTransactions
                allPositivebyYear = currentBacktestRecord.transactionPLbyYear




        


    t5 = time.clock()
    numberOfIterationsRemaining -= 1
    
    print('\nTotal number of iterations: ', numberOfIterations)
    print('Number of iterations remining: ', numberOfIterationsRemaining)
    print('Execution time: ',  t3 - t2)  
    print('Time remaining: ', (t3 - t2) * numberOfIterationsRemaining / 60, 'minutes\n')




print('\n')
print('Best mean $ return')
pprint.pprint(bestCombinationMean)
print('\n')
pprint.pprint(bestCombinationMeanbyYear)
print('\n')
pprint.pprint(bestCombinationMeanbyCurrency)
print('\n')
print('Best mean % return')
pprint.pprint(bestCombinationMeanPercent)
print('\n')
pprint.pprint(bestCombinationMeanPercentbyYear)
print('\n')
pprint.pprint(bestCombinationMeanPercentbyCurrency)
print('\n')
print('Best total return')
pprint.pprint(bestCombinationBalance)
print('\n')
pprint.pprint(bestCombinationBalancebyYear)
print('\n')
pprint.pprint(bestCombinationBalancebyCurrency)
print('\n')

if allPositive:
    print('All Positive')
    pprint.pprint(allPositive)
    print('\n')
    print('All Positive')
    print('\n')
    pprint.pprint(allPositivebyYear)
    print('\n')
    


print('Total execution time:   ', t5 - t4)
print('Number of iterations:   ', numberOfIterations)
print('Average iteration time: ', (t5 - t4) / numberOfIterations)





#print(transactionsData)
pickle.dump(currentBacktest.transactionsData, open('dataSave\\' + 'P&L', 'wb' ))
#pprint.pprint(currentBacktest.transactionsData)
#pprint.pprint(bestCombinationMean, parametersFile)
#pprint.pprint(bestCombinationBalance, parametersFile)
#pprint.pprint(bestCombinationOverall, parametersFile)
#parametersFile.close()







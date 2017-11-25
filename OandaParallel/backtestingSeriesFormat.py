import pprint
import indicators
import query
import pandas as pd
import numpy as np
import main
import time
import datetime
import itertools
import pickle
import dateList
import cython





transactionsData = pd.DataFrame()



#-----init------#
main.initialize()


#----main objects-----#


class backtest:


    def __init__(self, portfolio):
  
        #--------objects-----#

        self.portfolio  = portfolio

    
    def execute(self):
   
                  
        for (date, instrument) in self.data.keys():         
            
                row = self.data[(date, instrument)]

                self.monitor(row, instrument)
                                              
                                        #------------opens and closes transactions---------#

                if self.longConditions(row, instrument):                                   #open on conditions

                    if instrument in self.portfolio.openPositions and self.portfolio.openPositions[instrument].currentlyOpen == True:                       
                        self.portfolio.openPositions[instrument].close(row, instrument, tag = 'Long Conditions')
                                                                              
                    self.portfolio.openPositions[instrument] = position(self, instrument, row, 'Long')
                        
                        
                elif self.shortConditions(row, instrument):                                 #close on conditions
                        
                    if instrument in self.portfolio.openPositions and self.portfolio.openPositions[instrument].currentlyOpen == True:                       
                        self.portfolio.openPositions[instrument].close(row, instrument, tag = 'Short Conditions')
                              
                    self.portfolio.openPositions[instrument] = position(self, instrument, row, 'Short')   


    def longConditions(self, row, instrument):

        
        if (

            (row['longConditions'] == 1 and
             self.portfolio.transactionsCurrentlyOpen <= 1)
           
            and

            (instrument not in self.portfolio.openPositions  or 
            (instrument in self.portfolio.openPositions and self.portfolio.openPositions[instrument].direction != 'Long')) 
       

            ):           
            return True
        else:
            return False


    def closeLongConditions(self, row, instrument): 

        if (
            row['closeLongConditions'] == 1 and
            self.portfolio.openPositions[instrument].direction == 'Long' 
            ):                    
            return True
        else:
            return False

     
    def shortConditions(self, row, instrument):     


        if (

            (row['shortConditions'] == 1 and
             self.portfolio.transactionsCurrentlyOpen <= 1)
           
            and

            (instrument not in self.portfolio.openPositions  or 
            (instrument in self.portfolio.openPositions and self.portfolio.openPositions[instrument].direction != 'Short')) 
       

            ): 
            return True
        else:
            return False


    def closeShortConditions(self, row, instrument):

        if (
            row['closeShortConditions'] == 1 and
            self.portfolio.openPositions[instrument].direction == 'Short'
            ):
            return True
        else:
            return False


    def monitor(self, row, instrument):


        if instrument in self.portfolio.openPositions and self.portfolio.openPositions[instrument].currentlyOpen == True:


            self.portfolio.openPositions[instrument].status(row)

            #--------------------------trailing stops-----------------------#
          

            if (
                self.portfolio.openPositions[instrument].currentPL > (self.portfolio.openPositions[instrument].positionNotional * self.trailingStopRatio)            
                ):
                self.portfolio.openPositions[instrument].trailingStops(row)

            #--------------------stop loss and take profit------------------#



            if self.portfolio.openPositions[instrument].direction == 'Long':

                l = row['l']

                if  l < self.portfolio.openPositions[instrument].entryLow and self.portfolio.openPositions[instrument].entryLow > self.portfolio.openPositions[instrument].stopLoss:
                    self.portfolio.openPositions[instrument].close(row, instrument, entryValue = 'EL', tag = 'Entry Point')

                elif l < self.portfolio.openPositions[instrument].stopLoss:
                    self.portfolio.openPositions[instrument].close(row, instrument, maxValue = 'SL', tag = 'Stop Loss')

                elif self.portfolio.openPositions[instrument].trailingStopLoss != None:

                    if l < self.portfolio.openPositions[instrument].trailingStopLoss:

                        self.portfolio.openPositions[instrument].close(row, instrument, trailingValue = 'TSL', tag = 'Trailing stop Loss')

                
            elif self.portfolio.openPositions[instrument].direction == 'Short':

                h = row['h']

                if  h > self.portfolio.openPositions[instrument].entryHigh and self.portfolio.openPositions[instrument].entryHigh < self.portfolio.openPositions[instrument].stopLoss:
                    self.portfolio.openPositions[instrument].close(row, instrument, entryValue = 'EH', tag = 'Entry Point')

                elif h > self.portfolio.openPositions[instrument].stopLoss:
                    self.portfolio.openPositions[instrument].close(row, instrument, maxValue = 'SL', tag = 'Stop Loss')

                elif self.portfolio.openPositions[instrument].trailingStopLoss != None:

                    if h > self.portfolio.openPositions[instrument].trailingStopLoss:

                        self.portfolio.openPositions[instrument].close(row, instrument, trailingValue = 'TSL', tag = 'Trailing stop Loss')
      

 
            if instrument in self.portfolio.openPositions and self.portfolio.openPositions[instrument].currentlyOpen == True:

                  

                #if (           
                #    not self.longConditions(row, instrument) and 
                #    not self.shortConditions(row, instrument)
                #    ):


                #------long and short close conditions-----#

                if self.portfolio.openPositions[instrument].direction == 'Long':
                    if  self.closeLongConditions(row, instrument):
                        self.portfolio.openPositions[instrument].close(row, instrument, tag = 'Close long Conditions')

                elif self.portfolio.openPositions[instrument].direction == 'Short':
                    if self. closeShortConditions(row, instrument):
                        self.portfolio.openPositions[instrument].close(row, instrument, tag = 'Close short Conditions')                  



class backtestRecord:

    def __init__(self, backtest):

        self.backtest = backtest

        #update
        self.transaction = {}
        self.log = {}
        self.instrumentLog = {}

        #stats

        self.transactionStats = {}
        self.logStats = {}
        self.transactionsDuration = np.array([])
        self.transactionPLArray = np.array([])
        self.transactionPL100Array = np.array([])
 
    def update(self, instrument, tag, row):           #keeps a backtestRecord for each transaction

        self.transaction['Instrument:               ']  =                  self.backtest.portfolio.openPositions[instrument].instrument
        self.transaction['Entry Time:               ']  =                 (self.backtest.portfolio.openPositions[instrument].entryTime).to_pydatetime().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction['Entry Price:              ']  = '{:7.5f}'.format(self.backtest.portfolio.openPositions[instrument].entryPrice)
        self.transaction['Direction:                ']  =                  self.backtest.portfolio.openPositions[instrument].direction
        self.transaction['Number of units:          ']  = '{:7.5f}'.format(self.backtest.portfolio.openPositions[instrument].units)
        self.transaction['Exit Time:                ']  =                 (self.backtest.portfolio.openPositions[instrument].exitTime).to_pydatetime().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction['Exit Price:               ']  = '{:7.5f}'.format(self.backtest.portfolio.openPositions[instrument].exitPrice)
        self.transaction['Transaction $ return:     ']  = '${:,.2f}'.format(self.backtest.portfolio.openPositions[instrument].transactionPL)
        self.transaction['Transaction % return:     ']  = '%{:.4f}'.format(self.backtest.portfolio.openPositions[instrument].transactionPL100)
        self.transaction['Portfolio balance:        ']  = '${:,.2f}'.format(self.backtest.portfolio.balance)
        self.transaction['Reason closed:            ']  =                   tag
        self.transaction['Simultaneous positions:   ']  = (self.backtest.portfolio.transactionsCurrentlyOpen + 1)
        #self.transaction['Row:                      ']  =                   row
        
        self.log[self.backtest.portfolio.transactions] = dict(self.transaction)  
        self.instrumentLog[(instrument, self.backtest.portfolio.transactions)] = self.log[self.backtest.portfolio.transactions]
        
        #---------builds the array needed for the stats---------#

        self.transactionPLArray    = np.append(self.transactionPLArray,    self.backtest.portfolio.openPositions[instrument].transactionPL)
        self.transactionPL100Array = np.append(self.transactionPL100Array, self.backtest.portfolio.openPositions[instrument].transactionPL100)
        self.transactionPLArray = np.reshape(self.transactionPLArray, (-1 , 1))

        self.transactionsDuration  = np.append(self.transactionsDuration,    self.backtest.portfolio.openPositions[instrument].duration)
 
    def updateStats(self):      #keeps a backtestRecord for the entire backtest

       
        self.transactionStats['# of transactions:                '] = self.backtest.portfolio.transactions
        self.transactionStats['# of + transactions:              '] = self.backtest.portfolio.positiveTransactions
        self.transactionStats['# of - transactions:              '] = self.backtest.portfolio.negativeTransactions
        self.transactionStats['Ending balance:                   '] = '{:10,.5f}'.format(self.backtest.portfolio.balance)
        self.transactionStats['Transaction list:                 '] = {key:self.log[key]['Transaction $ return:     '] for key, value in self.log.items()}
        if self.transactionPLArray.size != 0 and self.transactionPL100Array.size != 0:
            self.transactionStats['Mean $ return:                    '] = '{:7,.5f}'.format(np.mean(self.transactionPLArray))
            self.transactionStats['Mean % return:                    '] = '{:7.5f}'.format(np.mean(self.transactionPL100Array))
            self.transactionStats['Mean duration:                    '] = '{:5<.2f} {}'.format(np.mean(self.transactionsDuration), 'hours')
            self.transactionStats['Std of return:                    '] = '{:7,.5f}'.format(np.std(self.transactionPLArray))
            self.transactionStats['Min return:                       '] = '{:7,.5f}'.format(np.min(self.transactionPLArray))
            self.transactionStats['Max return:                       '] = '{:7,.5f}'.format(np.max(self.transactionPLArray))
            self.transactionStats['Total P&L:                        '] = '{:7,.5f}'.format(np.sum(self.transactionPLArray))
        self.transactionStats['ATR ratio:                        '] = '{:7.5f}'.format(self.backtest.atrRatio)
        self.transactionStats['ADX level:                        '] = '{:7.5f}'.format(self.backtest.ADXLevelBelow)
        self.transactionStats['Candle range:                     '] = '{:7.5f}'.format(self.backtest.candleRange)
        self.transactionStats['Range Over deviation below:       '] = '{:7.5f}'.format(self.backtest.rangeOverDeviationBelow)
        self.transactionStats['Range Over deviation above:       '] = '{:7.5f}'.format(self.backtest.rangeOverDeviationAbove)
        self.transactionStats['Deviation ratio below:            '] = '{:7.5f}'.format(self.backtest.deviationRatioBelow)
        self.transactionStats['Deviation ratio above:            '] = '{:7.5f}'.format(self.backtest.deviationRatioAbove)
        self.transactionStats['RC close:                         '] = '{:7.5f}'.format(self.backtest.rcRatioClose)
        self.transactionStats['RC open:                          '] = '{:7.5f}'.format(self.backtest.rcRatioOpen)
        self.transactionStats['RC with direction on close:       '] = '{:7.5f}'.format(self.backtest.rcRatioCloseDirection)
        self.transactionStats['RC with direction on open:        '] = '{:7.5f}'.format(self.backtest.rcRatioOpenDirection)
        self.transactionStats['RSI oversold:                     '] = '{:7.5f}'.format(self.backtest.RSIOversold)
        self.transactionStats['RSI overbought:                   '] = '{:7.5f}'.format(self.backtest.RSIOverbought)
        self.transactionStats['RSI close overbought:             '] = '{:7.5f}'.format(self.backtest.RSIOverboughtClose)
        self.transactionStats['RSI close oversold:               '] = '{:7.5f}'.format(self.backtest.RSIOversoldClose)
        self.transactionStats['StochRSI overbought:              '] = '{:7.5f}'.format(self.backtest.StochRSIOverbought)
        self.transactionStats['StochRSI oversold:                '] = '{:7.5f}'.format(self.backtest.StochRSIOversold)
        self.transactionStats['StochRSI close overbought:        '] = '{:7.5f}'.format(self.backtest.StochRSIOverboughtClose)
        self.transactionStats['StochRSI close oversold:          '] = '{:7.5f}'.format(self.backtest.StochRSIOversoldClose)
        self.transactionStats['Stop loss @:                      '] = '{:7.4f}'.format(self.backtest.stopLossRatio)
        self.transactionStats['Take profit @:                    '] = '{:7.4f}'.format(self.backtest.takeProfitRatio)
        self.transactionStats['Trailing stop loss @:             '] = '{:7.4f}'.format(self.backtest.trailingStopRatio)
        
        


     

        self.logStats = dict(self.transactionStats) 



class portfolio:

    def __init__(self, balance):

        self.balance                   = balance
        self.startingBalance           = balance
        self.transactions              = 0
        self.positiveTransactions      = 0
        self.negativeTransactions      = 0
        self.transactionsCurrentlyOpen = 0
        self.openPositions             = {}
 

    def __str__(self): 

        #result = "\n".join({("{}: {}").format(key, self.__dict__[key]) for key, value in self.__dict__.items()})
        return 'Balance: '          + str(self.balance) + '\n' +   \
               'Transactions: '     + str(self.transactions)



class position:


    def __init__(self, backtest, instrument, row, direction):

        self.backtest         = backtest
        self.stopLossRatio    = self.backtest.stopLossRatio
        self.takeProfitRatio  = self.backtest.takeProfitRatio
        self.instrument       = instrument
        self.trailingStopLoss = None
        self.currentPL        = None


        self.entryPrice = row['c']
        self.entryTime  = row.name
        self.direction  = direction


        self.units            = ((self.backtest.portfolio.balance * 10) / self.entryPrice)
        self.positionNotional = self.units * self.entryPrice
        self.backtest.portfolio.transactionsCurrentlyOpen +=1

        self.currentlyOpen = True  

        

        self.stops(row)
      
    
    def close(self, row, instrument, tag, maxValue = None, entryValue = None, trailingValue = None):
        
        self.exitPrice  = row['c']
        self.exitTime   = row.name
        self.currentlyOpen = False 



        if   maxValue == None and entryValue == None and trailingValue == None:

            if self.direction == 'Long':
                self.transactionPL = (self.exitPrice - self.entryPrice) * self.units

            elif self.direction == 'Short':
                self.transactionPL = (self.entryPrice - self.exitPrice) * self.units

        elif maxValue == 'TP' and entryValue == None and trailingValue == None:

            self.exitPrice  = self.takeProfit

            if self.direction == 'Long':

                self.transactionPL = (self.takeProfit - self.entryPrice) * self.units

            elif self.direction == 'Short':

                self.transactionPL = (self.entryPrice - self.takeProfit) * self.units

        elif maxValue == 'SL' and entryValue == None and trailingValue == None:

            self.exitPrice = self.stopLoss

            if self.direction == 'Long':

                self.transactionPL = (self.stopLoss - self.entryPrice) * self.units

            elif self.direction == 'Short':

                self.transactionPL = (self.entryPrice - self.stopLoss) * self.units

        elif maxValue == None and entryValue == 'EL' and trailingValue == None:

            self.exitPrice = self.entryLow

            self.transactionPL = (self.entryLow - self.entryPrice) * self.units

        elif maxValue == None and entryValue == 'EH' and trailingValue == None:

            self.exitPrice = self.entryHigh

            self.transactionPL = (self.entryPrice - self.entryHigh) * self.units

        elif maxValue == None and entryValue == None and trailingValue == 'TSL':

            self.exitPrice = self.trailingStopLoss

            if self.direction == 'Long':
                self.transactionPL = (self.trailingStopLoss - self.entryPrice) * self.units

            elif self.direction == 'Short':
                self.transactionPL = (self.entryPrice - self.trailingStopLoss) * self.units


        if self.transactionPL != 0:
            self.transactionPL100 = self.transactionPL / (self.entryPrice * self.units)
        else:
            self.transactionPL100 = 0 
        self.backtest.portfolio.balance += self.transactionPL
        self.backtest.portfolio.transactions +=1
        self.backtest.portfolio.transactionsCurrentlyOpen -=1

        if self.transactionPL > 0:
            self.backtest.portfolio.positiveTransactions +=1
        else:
            self.backtest.portfolio.negativeTransactions +=1

        self.duration = self.exitTime - self.entryTime
        self.duration = self.duration.days

        currentBacktestRecord.update(instrument, tag, row)
        


        #global transactionsData
        #lastTransaction = pd.Series.to_frame(data[instrument].loc[self.entryTime])
        #lastTransaction = lastTransaction.transpose()
        #transactionsData = pd.concat([transactionsData, lastTransaction], axis = 0)
        #transactionsData.loc[self.entryTime, 'P&L'] = self.transactionPL
        #transactionsData.loc[self.entryTime, 'P&L100'] = self.transactionPL100
        #transactionsData.loc[self.entryTime, 'Direction'] = self.direction
        

        self.direction = None

    
    def status(self, row):

        c = row['c']
        h = row['h']
        l = row['l']

        if self.direction == 'Long':

            self.maxPLReached    = (h - self.entryPrice) * self.units 
            self.minPLReached    = (l - self.entryPrice) * self.units
            self.currentPL       = (c - self.entryPrice) * self.units

        elif self.direction == 'Short':
            
            self.maxPLReached    = (self.entryPrice - l) * self.units 
            self.minPLReached    = (self.entryPrice - h) * self.units 
            self.currentPL       = (self.entryPrice - c) * self.units 


    def stops(self, row): 

        c = row['c']

        if self.direction == 'Long':

            self.stopLoss         =  c - (self.backtest.stopLossRatio * c)
            self.takeProfit       =  c + (self.backtest.takeProfitRatio * c)

        elif self.direction == 'Short':

            self.stopLoss         =  c + (self.backtest.stopLossRatio * c)
            self.takeProfit       =  c - (self.backtest.takeProfitRatio * c)

        self.entryHigh  = row['h']#  + (row['h']  * 0.0003)
        self.entryLow   = row['l']#  - (row['l']  * 0.0003)


    def trailingStops(self, row):



        if self.direction == 'Long':

            #self.trailingStopLoss = self.entryPrice + (self.entryPrice * self.backtest.trailingStopRatio)
            self.trailingStopLoss = self.entryPrice

        elif self.direction == 'Short':

            #self.trailingStopLoss = self.entryPrice - (self.entryPrice * self.backtest.trailingStopRatio)
            self.trailingStopLoss = self.entryPrice


    def __str__(self): 

        result = "\n".join([("{}: {}").format(key, self.__dict__[key]) for key, value in sorted(self.__dict__.items())]) 

        return result


    def formatPrint(self):

        pprint.pprint(sorted(self.__dict__.items()))
        print('\n')





#-----data------#


startDate = datetime.datetime(2016, 12, 1, 0, 0, 0)
endDate   = datetime.datetime(2017, 7, 1, 0, 0, 0)
interval = 'H2'
offset   = None


if interval    == 'M15':
    dateList    = dateList.make15Minutes(startDate, endDate)
    offset      = 15
elif interval  == 'H1':
    dateList    = dateList.make1Hour(startDate, endDate)
    offset      = 60
elif interval  == 'H2':
    dateList    = dateList.make1Hour(startDate, endDate)
    offset      = 120
elif interval  == 'H4':
    dateList    = dateList.make1Hour(startDate, endDate)
    offset      = 240
elif interval  == 'D':
    dateList    = dateList.makeDays(startDate, endDate)
    offset      = 1440





def getData(startDate, endDate):

    t0 = time.clock()

    data_Object = main.dataObject()
    dataDict    = data_Object.dataBuild(interval, startDate, endDate, offset, \
    'AUD_NZD') #,'EUR_GBP','CAD_CHF', 'EUR_AUD', 'GBP_AUD', 'AUD_USD', 'AUD_NZD', 'CAD_CHF', 'EUR_CAD', 'EUR_USD', 'GBP_USD', 'USD_CAD', 'USD_JPY', 'USD_MXN', 'NZD_CAD', 'GBP_JPY' 
 
                                                                                                
    t1 = time.clock()
    print(t1 - t0)      

 
    #pickle.dump(dataDict, open('dataSave\\' + '4hours', 'wb' ))
    #dataDict = pickle.load(open( 'dataSave\\' + '2hours 2007-06-01 2017-07-01', 'rb'))

    return data_Object, dataDict 

data_Object, dataDict = getData(startDate, endDate)
data = dataDict.copy()




    
for instrument in data.keys():
     
    if interval == 'D':

        data[instrument].index = pd.DatetimeIndex(data[instrument].index).normalize()
                         
    data[instrument] =  data_Object.setIndicators(data[instrument],

    ('RSI', 7), 
    ('RSI', 12),
    ('StochRSI', 14, 3, 3), 
    ('EMA', 'Price', 10), 
    ('EMA', 'Price', 20), 
    ('EMA', 'Price', 200),
    ('EMA', 'Price', 365), 
    ('EMA', 'Price', 400),
    ('EMA', 'Volume', 5), 
    ('EMA', 'Volume', 10), 
    ('EMA', 'Volume', 20),
    ('BearishRC',),
    ('BullishRC',),
    ('Highest Price', 10),
    ('Lowest Price', 10), 
    ('Highest Price', 20), 
    ('Lowest Price', 20),
    ('ADX', 6),
    ('ADX', 12), 
    ('ADX', 14),
    ('Deviation', 10),
    ('Deviation', 20),
    ('Deviation', 40), 
    ('Deviation', 50), 
    ('Deviation', 100), 
    ('Deviation', 200),
    ('Bollinger Bands', 20, 2.5))
    #data[instrument]['pythonDate'] = data[instrument].index.to_pydatetime()
    #print(data[instrument].index)


    data[instrument] = data[instrument][np.isfinite(data[instrument]['PriceEMA365'])]
    #data[instrument].to_excel('dataSave\\' + str(instrument) + '.xlsx')
    #print(data[instrument]['2016-12-28 00:00:00': '2017-01-04 00:00:00'])


#-----data------#


#-----run-------#

bestCombinationMean = {}
bestCombinationBalance = {}
bestCombinationOverall = {}
maxMeanReturn = 0
maxEndingBalance = 0
maxMeanOverall = 0
maxBalanceOverall = 0


seriesAlreadySet = False

parametersFile = open('dataSave\\' + 'transactiondata.txt', "w")

for rcRatioClose,               \
    rcRatioOpen,                \
    rcRatioCloseDirection,      \
    rcRatioOpenDirection,       \
    atrRatio,                   \
    RSIOversold,                \
    RSIOverbought,              \
    StochRSIOversold,           \
    StochRSIOverbought,         \
    RSIOversoldClose,           \
    RSIOverboughtClose,         \
    StochRSIOversoldClose,      \
    StochRSIOverboughtClose,    \
    stopLossRatio,              \
    takeProfitRatio,            \
    trailingStopRatio,          \
    deviationRatioBelow,        \
    deviationRatioAbove,        \
    candleRange,                \
     rangeOverDeviationBelow,   \
     rangeOverDeviationAbove,   \
     ADXLevelBelow                   \
                                \
    in itertools.product(             
    [0.3],    #rcRatioClose
    [0.3],    #rcRatioOpen
    [0.42],    #rcRatioCloseDirection
    [0.58],    #rcRatioOpenDirection
    [1.22],    #atrRatio
    [30],      #RSIOversold
    [70],      #RSIOverbought
    [12],      #StochRSIOversold
    [88],      #StochRSIOverbought
    [30],      #RSIOversoldClose
    [70],      #RSIOverboughtClose
    [10],      #StochRSIOversoldClose
    [90],      #StochRSIOverboughtClose
    [0.002],   #stopLossRatio
    [0.05],    #takeProfitRatio
    [0.0075],  #trailingStopRatio
    [0.0055],  #deviationRatioBelow
    [0.0015],  #deviationRatioAbove
    [1.05],    #candleRange
    [10],      #rangeOverDeviationBelow
    [0],       #rangeOverDeviationAbove
    [35]       #ADXLeve
    ):    
 
    
        

    #----main objects initializing-----#
    currentPortfolio        = portfolio(10000)
    currentBacktest         = backtest(currentPortfolio)                            #composite object
    currentBacktestRecord   = backtestRecord(currentBacktest)                       #to gain access to currentBacktest data
        
    #-----execute------#
         
    def setBacktestParameters(currentBacktest):
        currentBacktest.dateList                = dateList
        currentBacktest.stopLossRatio           = stopLossRatio
        currentBacktest.takeProfitRatio         = takeProfitRatio
        currentBacktest.trailingStopRatio       = trailingStopRatio
        currentBacktest.rcRatioClose            = rcRatioClose
        currentBacktest.rcRatioOpen             = rcRatioOpen
        currentBacktest.rcRatioCloseDirection   = rcRatioCloseDirection
        currentBacktest.rcRatioOpenDirection    = rcRatioOpenDirection
        currentBacktest.atrRatio                = atrRatio
        currentBacktest.ADXLevelBelow                = ADXLevelBelow
        currentBacktest.candleRange             = candleRange
        currentBacktest.rangeOverDeviationBelow = rangeOverDeviationBelow
        currentBacktest.rangeOverDeviationAbove = rangeOverDeviationAbove
        currentBacktest.deviationRatioBelow     = deviationRatioBelow
        currentBacktest.deviationRatioAbove     = deviationRatioAbove
        currentBacktest.RSIOversold             = RSIOversold
        currentBacktest.RSIOverbought           = RSIOverbought
        currentBacktest.RSIOversoldClose        = RSIOversoldClose
        currentBacktest.RSIOverboughtClose      = RSIOverboughtClose
        currentBacktest.StochRSIOversold        = StochRSIOversold
        currentBacktest.StochRSIOverbought      = StochRSIOverbought
        currentBacktest.StochRSIOversoldClose   = StochRSIOversoldClose
        currentBacktest.StochRSIOverboughtClose = StochRSIOverboughtClose

        return currentBacktest

    currentBacktest = setBacktestParameters(currentBacktest)
    
    def applyConditions(data):

        #longconditions

        for instrument in data.keys():

            data[instrument] =  data[instrument].assign(longConditions = np.where((

           (#row['VolumeEMA5'] > row['VolumeEMA20']                              and
            (data[instrument]['RSI7'] < RSIOversold)                             &
            (data[instrument]['StochRSI_K14/3'] < StochRSIOversold)                &
           #(row['h'] - row['l']) >= (row['ATR14'] * self.atrRatio)              and
           #(row['h'] - row['l']) <= (row['ATR14'] * 5)                          and
            #row['c'] > row['PriceEMA150']                                      and
            #row['l'] < row['LowerBB20/3']                                      and
            #row['Deviation%40'] < self.deviationRatioBelow                      and
            #row['Deviation%40'] > self.deviationRatioAbove                      and
            #row['HLOverDeviation40'] < rangeOverDeviationBelow                  and
            #row['HLOverDeviation40'] > rangeOverDeviationAbove                  and
            #row['PriceEMA10'] < row['PriceEMA20']                              and
            #row['ADX14'] < 35                                                   and
            #row['ADX14'] > 15                                                   and
           #(row['h'] / row['l']) < self.candleRange                             and
            (data[instrument]['BullishRejectionCandleClose'] <= rcRatioClose)      &
            (data[instrument]['BullishRejectionCandleOpen']  <= rcRatioOpen))

            |

            ((data[instrument]['VolumeEMA5'] > data[instrument]['VolumeEMA20'])     &
            #row['RSI7'] < self.RSIOversold                                      and
            (data[instrument]['StochRSI_K14/3'] < StochRSIOversold)                &
           #(row['h'] - row['l']) >= (row['ATR14'] * self.atrRatio)              and
           #(row['h'] - row['l']) <= (row['ATR14'] * 5)                          and
            #row['c'] > row['PriceEMA150']                                       and
            #row['l'] < row['LowerBB20/3']                                     and
            #row['Deviation%40'] < self.deviationRatioBelow                      and
            #row['Deviation%40'] > self.deviationRatioAbove                      and
            #row['HLOverDeviation40'] < rangeOverDeviationBelow                  and
            #row['HLOverDeviation40'] > rangeOverDeviationAbove                  and
            #row['PriceEMA10'] < row['PriceEMA20']                               and
            #row['ADX14'] < 35                                                   and
            #row['ADX14'] > 15                                                   and
            #(row['h'] / row['l']) < self.candleRange                            and
            (data[instrument]['BullishRejectionCandleClose'] <= rcRatioCloseDirection)    &
            (data[instrument]['BullishRejectionCandleOpen']  <= rcRatioOpenDirection)      &  
            (data[instrument]['c'] > data[instrument]['o'])))

             , 1, 0))
        
        #shortconditions

        for instrument in data.keys():

            data[instrument] =  data[instrument].assign(shortConditions = np.where((

           (# row['VolumeEMA5'] < row['VolumeEMA20']                              and
            (data[instrument]['RSI7'] > RSIOverbought)                            &
            (data[instrument]['StochRSI_K14/3'] > StochRSIOverbought)             &
          # (row['h'] - row['l']) >= (row['ATR14'] * self.atrRatio)              and
          # (row['h'] - row['l']) <= (row['ATR14'] * 5)                          and
            #row['c'] < row['PriceEMA150']                                      and
            #row['h'] > row['UpperBB20/3']                                      and
           #row['Deviation%40'] < self.deviationRatioBelow                      and
            #row['Deviation%40'] > self.deviationRatioAbove                      and
            #row['HLOverDeviation40'] < rangeOverDeviationBelow                  and
            #row['HLOverDeviation40'] > rangeOverDeviationAbove                  and
            #row['PriceEMA10'] > row['PriceEMA20']                              and
            #row['ADX14'] < 35                                                   and
            #row['ADX14'] > 15                                                   and
            #(row['h'] / row['l']) < self.candleRange                            and
            (data[instrument]['BearishRejectionCandleClose'] <= rcRatioClose)     &
            (data[instrument]['BearishRejectionCandleOpen']  <= rcRatioOpen))

            |

            ((#row['VolumeEMA5'] < row['VolumeEMA20']                              and
            #row['RSI7'] > self.RSIOverbought                                   and
            (data[instrument]['StochRSI_K14/3'] > StochRSIOverbought)       &
           #(row['h'] - row['l']) >= (row['ATR14'] * self.atrRatio)              and
           #(row['h'] - row['l']) <= (row['ATR14'] * 5)                          and
            #row['c'] < row['PriceEMA150']                                       and
            #row['h'] > row['UpperBB20/3']                                     and
            #row['Deviation%40'] < self.deviationRatioBelow                      and
            #row['Deviation%40'] > self.deviationRatioAbove                      and
            #row['HLOverDeviation40'] < rangeOverDeviationBelow                  and
            #row['HLOverDeviation40'] > rangeOverDeviationAbove                  and
            #row['PriceEMA10'] > row['PriceEMA20']                               and
            #row['ADX14'] < 35                                                   and
           # row['ADX14'] > 15                                                   and
           # (row['h'] / row['l']) < self.candleRange                            and
            (data[instrument]['BearishRejectionCandleClose'] <= rcRatioCloseDirection)    &
            (data[instrument]['BearishRejectionCandleOpen']  <= rcRatioOpenDirection)    &    
            (data[instrument]['c'] < data[instrument]['o']))))

             , 1, 0))

        #closeLongconditions

        for instrument in data.keys():

            data[instrument] =  data[instrument].assign(closeLongConditions = np.where((

           (#self.portfolio.openPositions[instrument].currentPL > 0       and 
            (data[instrument]['StochRSI_K14/3'] > StochRSIOverboughtClose)   &
            (data[instrument]['RSI7'] > RSIOverboughtClose  ))

            |

            ((data[instrument]['BearishRejectionCandleClose'] <= rcRatioClose)              &
            (data[instrument]['BearishRejectionCandleOpen']  <=  rcRatioOpen)               &
            ((data[instrument]['h'] - data[instrument]['l']) >= (data[instrument]['ATR14'] * atrRatio))))

             , 1, 0))

        #closeShortconditions

        for instrument in data.keys():

            data[instrument] =  data[instrument].assign(closeShortConditions = np.where((

           (#self.portfolio.openPositions[instrument].currentPL > 0       and 
            (data[instrument]['StochRSI_K14/3'] < StochRSIOversoldClose)   &
            (data[instrument]['RSI7'] < RSIOversoldClose  ))

            |

            ((data[instrument]['BullishRejectionCandleClose'] <= rcRatioClose)              &
            (data[instrument]['BullishRejectionCandleOpen']   <=  rcRatioOpen)               &
            ((data[instrument]['h'] - data[instrument]['l']) >= (data[instrument]['ATR14'] * atrRatio))))

             , 1, 0))

        return data
    applyConditions(data)

    if seriesAlreadySet == False:

        #itemsSet = [(date, instrument) for date in dateList for instrument in data.keys() if date in data[instrument].index] 

        
        dataDictSeries = {}
        for date in dateList:
            for instrument in data.keys():
                if date in data[instrument].index:
                    dataDictSeries[(date, instrument)] = data[instrument].ix[date]
        data = dataDictSeries.copy()
        seriesAlreadySet = True


    currentBacktest.data  = data
    t2 = time.clock()
    currentBacktest.execute()
    t3 = time.clock()
    print('Execution time: ', t3 - t2)
      
                    

    #-----shutdown per parameters set-----#

    def shutDownParametersSet():

        currentBacktestRecord.updateStats()      

    #-----printStuff per parameters set-----#

        pprint.pprint(currentBacktestRecord.log, indent = 1)
        #pprint.pprint(currentBacktestRecord.instrumentLog, indent = 1)
        pprint.pprint(currentBacktestRecord.logStats, indent = 1)
        pprint.pprint(currentBacktestRecord.log, parametersFile)
        return None

    shutDownParametersSet()
 
    #-----shutdown per backtest------# 
   
    def shutDownBacktest(bestCombinationMean, bestCombinationBalance, bestCombinationOverall, maxMeanReturn, maxEndingBalance, maxMeanOverall, maxBalanceOverall ):

        if currentBacktestRecord.transactionPLArray .size != 0:

            if  np.mean(currentBacktestRecord.transactionPLArray) > maxMeanReturn:
                maxMeanReturn = np.mean(currentBacktestRecord.transactionPLArray)
                bestCombinationMean = currentBacktestRecord.logStats

            if  currentBacktest.portfolio.balance > maxEndingBalance:
                maxEndingBalance = currentBacktest.portfolio.balance
                bestCombinationBalance = currentBacktestRecord.logStats
        
            if  currentBacktest.portfolio.balance > maxBalanceOverall and np.mean(currentBacktestRecord.transactionPLArray) > maxMeanOverall:
                maxBalanceOverall = currentBacktest.portfolio.balance
                maxMeanOverall = np.mean(currentBacktestRecord.transactionPLArray)
                bestCombinationOverall = currentBacktestRecord.logStats 


        return bestCombinationMean, bestCombinationBalance, bestCombinationOverall, maxMeanReturn, maxEndingBalance, maxBalanceOverall, maxMeanOverall
  

    bestCombinationMean,    \
    bestCombinationBalance, \
    bestCombinationOverall, \
    maxMeanReturn,          \
    maxEndingBalance,       \
    maxMeanOverall,         \
    maxBalanceOverall       \
    = shutDownBacktest(bestCombinationMean, bestCombinationBalance, bestCombinationOverall, maxMeanReturn, maxEndingBalance, maxMeanOverall, maxBalanceOverall)





print('\n')
print('Best mean $ return')
pprint.pprint(bestCombinationMean)
print('\n')
print('Best total return')
pprint.pprint(bestCombinationBalance)
print('Best total overall')
pprint.pprint(bestCombinationOverall)

print('Execution time: ', t3 - t2)


#print(transactionsData)
#pickle.dump(transactionsData, open('dataSave\\' + 'P&L', 'wb' ))
#pprint.pprint(bestCombinationMean, parametersFile)
#pprint.pprint(bestCombinationBalance, parametersFile)
#pprint.pprint(bestCombinationOverall, parametersFile)
#parametersFile.close()







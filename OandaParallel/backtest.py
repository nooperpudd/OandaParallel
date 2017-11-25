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
import conditions
import pprint









#-----init------#
main.initialize()


#----main objects-----#
class backtest:


    def __init__(self, portfolio):
  
        #--------objects-----#

        self.portfolio = portfolio
        self.transactionsData = pd.DataFrame()
    
    def execute(self):
   
                  
        for (date, instrument) in self.data.keys():         
            
                row = self.data[(date, instrument)]

                self.monitor(row, instrument, date)
                                              
                                        #------------opens and closes
                                        #transactions---------#



                if conditions.longConditions(self, row, instrument):                                   


                    if instrument in self.portfolio.openPositions and self.portfolio.openPositions[instrument].currentlyOpen == True:                       
                        self.portfolio.openPositions[instrument].close(row, instrument, date, tag = 'Long Conditions')
                                                                              
                    self.portfolio.openPositions[instrument] = position(self, instrument, row, date, 'Long')
                        
                        
                elif conditions.shortConditions(self, row, instrument):                                  

                        
                    if instrument in self.portfolio.openPositions and self.portfolio.openPositions[instrument].currentlyOpen == True:                       
                        self.portfolio.openPositions[instrument].close(row, instrument, date, tag = 'Short Conditions')
                              
                    self.portfolio.openPositions[instrument] = position(self, instrument, row, date, 'Short') 
                    

    def monitor(self, row, instrument, date):


        if instrument in self.portfolio.openPositions and self.portfolio.openPositions[instrument].currentlyOpen == True:

          

            self.portfolio.openPositions[instrument].status(row, date)

            #--------------------------trailing stops-----------------------#
          

            if self.portfolio.openPositions[instrument].openTag != 'Regression Channel':

                if (self.portfolio.openPositions[instrument].currentPL > (self.portfolio.openPositions[instrument].positionNotional * self.trailingStopRatio)):
                    self.portfolio.openPositions[instrument].trailingStops(row)

            elif self.portfolio.openPositions[instrument].openTag == 'Regression Channel':

                if (self.portfolio.openPositions[instrument].currentPL > (self.portfolio.openPositions[instrument].positionNotional * self.channelTrailingStopRatio)):
                    self.portfolio.openPositions[instrument].trailingStops(row)


            #--------------------stop loss and take profit------------------#

            #----------------------regression channel-----------------------#

            h = row['h']
            l = row['l']
            c = row['c']

            if self.portfolio.openPositions[instrument].openTag == 'Regression Channel':

                self.portfolio.openPositions[instrument].channelRegressionTakeProfit += self.portfolio.openPositions[instrument].regressionBeta
                self.portfolio.openPositions[instrument].channelRegressionStopLoss   += self.portfolio.openPositions[instrument].regressionBeta

                if self.portfolio.openPositions[instrument].direction == 'Long':

                    if (l < self.portfolio.openPositions[instrument].entryLow and self.portfolio.openPositions[instrument].entryLow > self.portfolio.openPositions[instrument].channelStopLoss):
                        self.portfolio.openPositions[instrument].close(row, instrument, date, entryValue = 'EL', tag = 'Entry Point')
                    

                    elif (c < self.portfolio.openPositions[instrument].channelRegressionStopLoss and l > self.portfolio.openPositions[instrument].channelStopLoss):
                            self.portfolio.openPositions[instrument].close(row, instrument, date, maxValue = 'CRSL', tag = 'Channel Regression Stop Loss')

                    elif l < self.portfolio.openPositions[instrument].channelStopLoss:
                        self.portfolio.openPositions[instrument].close(row, instrument, date, maxValue = 'CSL', tag = 'Channel Stop Loss')


                    elif (h > self.portfolio.openPositions[instrument].channelRegressionTakeProfit and self.portfolio.openPositions[instrument].channelRegressionTakeProfit < self.portfolio.openPositions[instrument].channelTakeProfit):
                        self.portfolio.openPositions[instrument].close(row, instrument, date, maxValue = 'CRTP', tag = 'Channel Regression Take Profit')


                    elif h > self.portfolio.openPositions[instrument].channelTakeProfit:
                        self.portfolio.openPositions[instrument].close(row, instrument, date, maxValue = 'CTP', tag = 'Channel Take Profit')



                    elif self.portfolio.openPositions[instrument].channelTrailingStopLoss != None:

                        if l < self.portfolio.openPositions[instrument].channelTrailingStopLoss:

                            self.portfolio.openPositions[instrument].close(row, instrument, date,  trailingValue = 'CTSL', tag = 'Channel Trailing Stop Loss')



                elif self.portfolio.openPositions[instrument].direction == 'Short':

                    if (h > self.portfolio.openPositions[instrument].entryHigh and self.portfolio.openPositions[instrument].entryHigh < self.portfolio.openPositions[instrument].channelStopLoss):
                        self.portfolio.openPositions[instrument].close(row, instrument, date, entryValue = 'EH', tag = 'Entry Point')

                    elif (c > self.portfolio.openPositions[instrument].channelRegressionStopLoss and h < self.portfolio.openPositions[instrument].channelStopLoss):
                            self.portfolio.openPositions[instrument].close(row, instrument, date, maxValue = 'CRSL', tag = 'Channel Regression Stop Loss')

                    elif h > self.portfolio.openPositions[instrument].channelStopLoss:
                        self.portfolio.openPositions[instrument].close(row, instrument, date, maxValue = 'CSL', tag = 'Channel Stop Loss')

                    elif (l < self.portfolio.openPositions[instrument].channelRegressionTakeProfit and self.portfolio.openPositions[instrument].channelRegressionTakeProfit > self.portfolio.openPositions[instrument].channelTakeProfit):
                        self.portfolio.openPositions[instrument].close(row, instrument, date, maxValue = 'CRTP', tag = 'Channel Regression Take Profit')


                    elif l < self.portfolio.openPositions[instrument].channelTakeProfit:
                        self.portfolio.openPositions[instrument].close(row, instrument, date, maxValue = 'CTP', tag = 'Channel Take Profit')



                    elif self.portfolio.openPositions[instrument].channelTrailingStopLoss != None:

                        if h > self.portfolio.openPositions[instrument].channelTrailingStopLoss:

                            self.portfolio.openPositions[instrument].close(row, instrument, date,  trailingValue = 'CTSL', tag = 'Channel Trailing Stop Loss')

                    

                #self.numberPeriodsOpen = (date -
                #self.portfolio.openPositions[instrument].entryTime).seconds/3600/self.interval



            #--------------------------price action-----------------------#

            elif self.portfolio.openPositions[instrument].openTag == 'Rejection EMA':


                if self.portfolio.openPositions[instrument].direction == 'Long':
                
                            

                    if l < self.portfolio.openPositions[instrument].stopLoss:
                        self.portfolio.openPositions[instrument].close(row, instrument, date, maxValue = 'SL', tag = 'Stop Loss')

                    elif h > self.portfolio.openPositions[instrument].takeProfit:
                        self.portfolio.openPositions[instrument].close(row, instrument, date, maxValue = 'TP', tag = 'Take Profit')

                    #elif self.portfolio.openPositions[instrument].trailingStopLoss != None:

                    #    if l < self.portfolio.openPositions[instrument].trailingStopLoss:

                    #        self.portfolio.openPositions[instrument].close(row, instrument, date,  trailingValue = 'TSL', tag = 'Trailing stop Loss')

                
                elif self.portfolio.openPositions[instrument].direction == 'Short':
              
               

                    if h > self.portfolio.openPositions[instrument].stopLoss:
                        self.portfolio.openPositions[instrument].close(row, instrument, date, maxValue = 'SL', tag = 'Stop Loss')

                    elif l < self.portfolio.openPositions[instrument].takeProfit:
                        self.portfolio.openPositions[instrument].close(row, instrument, date, maxValue = 'TP', tag = 'Take Profit')

                    #elif self.portfolio.openPositions[instrument].trailingStopLoss != None:

                    #    if h > self.portfolio.openPositions[instrument].trailingStopLoss:

                    #        self.portfolio.openPositions[instrument].close(row, instrument, date, trailingValue = 'TSL', tag = 'Trailing stop Loss')    

            
            else:


                if self.portfolio.openPositions[instrument].direction == 'Long':
                
                

                    if  l < self.portfolio.openPositions[instrument].entryLow and self.portfolio.openPositions[instrument].entryLow > self.portfolio.openPositions[instrument].stopLoss:
                        self.portfolio.openPositions[instrument].close(row, instrument, date, entryValue = 'EL', tag = 'Entry Point')                 

                    elif l < self.portfolio.openPositions[instrument].stopLoss:
                        self.portfolio.openPositions[instrument].close(row, instrument, date, maxValue = 'SL', tag = 'Stop Loss')

                    elif h > self.portfolio.openPositions[instrument].takeProfit:
                        self.portfolio.openPositions[instrument].close(row, instrument, date, maxValue = 'TP', tag = 'Take Profit')

                    #elif self.portfolio.openPositions[instrument].trailingStopLoss != None:

                    #    if l < self.portfolio.openPositions[instrument].trailingStopLoss:

                    #        self.portfolio.openPositions[instrument].close(row, instrument, date,  trailingValue = 'TSL', tag = 'Trailing stop Loss')

                
                elif self.portfolio.openPositions[instrument].direction == 'Short':
              
                

                    if  h > self.portfolio.openPositions[instrument].entryHigh and self.portfolio.openPositions[instrument].entryHigh < self.portfolio.openPositions[instrument].stopLoss:
                        self.portfolio.openPositions[instrument].close(row, instrument, date, entryValue = 'EH', tag = 'Entry Point')


                    elif h > self.portfolio.openPositions[instrument].stopLoss:
                        self.portfolio.openPositions[instrument].close(row, instrument, date, maxValue = 'SL', tag = 'Stop Loss')

                    elif l < self.portfolio.openPositions[instrument].takeProfit:
                        self.portfolio.openPositions[instrument].close(row, instrument, date, maxValue = 'TP', tag = 'Take Profit')

                    #elif self.portfolio.openPositions[instrument].trailingStopLoss != None:

                    #    if h > self.portfolio.openPositions[instrument].trailingStopLoss:

                    #        self.portfolio.openPositions[instrument].close(row, instrument, date, trailingValue = 'TSL', tag = 'Trailing stop Loss')
      

 
            if instrument in self.portfolio.openPositions and self.portfolio.openPositions[instrument].currentlyOpen == True:

                  

                #if (
                #    not self.longConditions(row, instrument) and
                #    not self.shortConditions(row, instrument)
                #    ):


                #------long and short close conditions-----#

                if self.portfolio.openPositions[instrument].direction == 'Long':
                    if  conditions.closeLongConditions(self, row, instrument):
                        self.portfolio.openPositions[instrument].close(row, instrument, date, tag = 'Close long Conditions')

                elif self.portfolio.openPositions[instrument].direction == 'Short':
                    if conditions.closeShortConditions(self, row, instrument):
                        self.portfolio.openPositions[instrument].close(row, instrument, date, tag = 'Close short Conditions')    
                        

class position:


    def __init__(self, backtest, instrument, row, date, direction):

        self.backtest = backtest
        self.instrument = instrument
        self.trailingStopLoss = None
        self.channelTrailingStopLoss = None
        self.currentPL = None
        self.openRow = row


        self.entryPrice = row['c']
        self.entryTime = date
        self.direction = direction
        

        self.units = ((self.backtest.portfolio.balance * 1) / self.entryPrice)
        self.positionNotional = self.units * self.entryPrice
        self.backtest.portfolio.transactionsCurrentlyOpen +=1


        self.openTag = self.backtest.openTag


        if self.openTag == 'Regression Channel':
            self.channelStopAndTakeProfit(row)

        elif self.openTag == 'Rejection EMA':
            self.EMAstopAndTakeProfit(row)
     
        elif self.openTag != 'Regression Channel' and self.openTag != 'Rejection EMA':
            self.stopAndTakeProfit(row)
        
        
        self.currentlyOpen = True  
    

    def close(self, row, instrument, date, tag, maxValue=None, entryValue=None, trailingValue=None):
        
        self.exitPrice = row['c']
        self.exitTime = date
        self.currentlyOpen = False 


        if   maxValue == 'SL' and entryValue == None and trailingValue == None:

            self.exitPrice = self.stopLoss

            if self.direction == 'Long':

                self.transactionPL = (self.stopLoss - self.entryPrice) * self.units

            elif self.direction == 'Short':

                self.transactionPL = (self.entryPrice - self.stopLoss) * self.units

        elif maxValue == 'CSL' and entryValue == None and trailingValue == None:

            self.exitPrice = self.channelStopLoss

            if self.direction == 'Long':

                self.transactionPL = (self.channelStopLoss - self.entryPrice) * self.units

            elif self.direction == 'Short':

                self.transactionPL = (self.entryPrice - self.channelStopLoss) * self.units

        elif maxValue == None and entryValue == None and trailingValue == None:

            if self.direction == 'Long':
                self.transactionPL = (self.exitPrice - self.entryPrice) * self.units

            elif self.direction == 'Short':
                self.transactionPL = (self.entryPrice - self.exitPrice) * self.units

        elif maxValue == None and entryValue == 'EL' and trailingValue == None:

            self.exitPrice = self.entryLow

            self.transactionPL = (self.entryLow - self.entryPrice) * self.units

        elif maxValue == None and entryValue == 'EH' and trailingValue == None:

            self.exitPrice = self.entryHigh

            self.transactionPL = (self.entryPrice - self.entryHigh) * self.units

        elif maxValue == 'TP' and entryValue == None and trailingValue == None:

            self.exitPrice = self.takeProfit

            if self.direction == 'Long':

                self.transactionPL = (self.takeProfit - self.entryPrice) * self.units

            elif self.direction == 'Short':

                self.transactionPL = (self.entryPrice - self.takeProfit) * self.units

        elif maxValue == 'CTP' and entryValue == None and trailingValue == None:

            self.exitPrice = self.channelTakeProfit

            if self.direction == 'Long':

                self.transactionPL = (self.channelTakeProfit - self.entryPrice) * self.units

            elif self.direction == 'Short':

                self.transactionPL = (self.entryPrice - self.channelTakeProfit) * self.units

        elif maxValue == 'CRTP' and entryValue == None and trailingValue == None:

            self.exitPrice = self.channelRegressionTakeProfit

            if self.direction == 'Long':

                self.transactionPL = (self.channelRegressionTakeProfit - self.entryPrice) * self.units

            elif self.direction == 'Short':

                self.transactionPL = (self.entryPrice - self.channelRegressionTakeProfit) * self.units
      
        elif maxValue == 'CRSL' and entryValue == None and trailingValue == None:

            self.exitPrice = row['c']

            if self.direction == 'Long':

                self.transactionPL = (self.exitPrice - self.entryPrice) * self.units

            elif self.direction == 'Short':

                self.transactionPL = (self.entryPrice - self.exitPrice) * self.units

        elif maxValue == None and entryValue == None and trailingValue == 'TSL':

            self.exitPrice = self.trailingStopLoss

            if self.direction == 'Long':
                self.transactionPL = (self.trailingStopLoss - self.entryPrice) * self.units

            elif self.direction == 'Short':
                self.transactionPL = (self.entryPrice - self.trailingStopLoss) * self.units

        elif maxValue == None and entryValue == None and trailingValue == 'CTSL':

            self.exitPrice = self.channelTrailingStopLoss

            if self.direction == 'Long':
                self.transactionPL = (self.channelTrailingStopLoss - self.entryPrice) * self.units

            elif self.direction == 'Short':
                self.transactionPL = (self.entryPrice - self.channelTrailingStopLoss) * self.units



        self.backtest.portfolio.balance += self.transactionPL
        self.backtest.portfolio.transactions +=1
        self.backtest.portfolio.transactionsCurrentlyOpen -=1

        if self.transactionPL < 0:

            self.backtest.portfolio.negativeTransactions +=1
            self.transactionPL100 = self.transactionPL / (self.entryPrice * self.units)

        elif self.transactionPL > 0:

            self.backtest.portfolio.positiveTransactions +=1
            self.transactionPL100 = self.transactionPL / (self.entryPrice * self.units)

        else:

            self.backtest.portfolio.breakEvenTransactions +=1
            self.transactionPL100 = 0
        

        self.duration = self.exitTime - self.entryTime
        #self.duration = self.duration.days


        self.backtest.backtestRecord.update(instrument, tag, row)
                


        lastTransaction = pd.Series(self.backtest.data[(self.entryTime, instrument)])
        lastTransaction = pd.Series.to_frame(lastTransaction)
        lastTransaction = lastTransaction.transpose()
        lastTransaction['date'] = self.entryTime
        lastTransaction['instrument'] = instrument
        lastTransaction.set_index('date', inplace = True)
        self.backtest.transactionsData = pd.concat([self.backtest.transactionsData, lastTransaction], axis = 0)
        self.backtest.transactionsData.loc[self.entryTime, 'P&L'] = self.transactionPL
        self.backtest.transactionsData.loc[self.entryTime, 'P&L100'] = self.transactionPL100
        self.backtest.transactionsData.loc[self.entryTime, 'Direction'] = self.direction
        

        self.direction = None

    
    def status(self, row, date):

        c = row['c']
        h = row['h']
        l = row['l']
                

        if self.direction == 'Long':

            self.maxPLReached = (h - self.entryPrice) * self.units 
            self.minPLReached = (l - self.entryPrice) * self.units
            self.currentPL = (c - self.entryPrice) * self.units

        elif self.direction == 'Short':
            
            self.maxPLReached = (self.entryPrice - l) * self.units 
            self.minPLReached = (self.entryPrice - h) * self.units 
            self.currentPL = (self.entryPrice - c) * self.units 


    def stopAndTakeProfit(self, row): 

        c = row['c']

        if self.direction == 'Long':

            self.stopLoss = c - (self.backtest.stopLossRatio * c)
            self.takeProfit = c + (self.backtest.takeProfitRatio * c)

        elif self.direction == 'Short':

            self.stopLoss = c + (self.backtest.stopLossRatio * c)
            self.takeProfit = c - (self.backtest.takeProfitRatio * c)

        self.entryHigh = row['h']#  + (row['h'] * 0.0003)
        self.entryLow = row['l']#  - (row['l'] * 0.0003)


    def EMAstopAndTakeProfit(self, row): 

        c = row['c']

        if self.direction == 'Long':

            self.stopLoss = c - (self.backtest.EMAstopLossRatio * c)
            self.takeProfit = c + (self.backtest.EMAtakeProfitRatio * c)

        elif self.direction == 'Short':

            self.stopLoss = c + (self.backtest.EMAstopLossRatio * c)
            self.takeProfit = c - (self.backtest.EMAtakeProfitRatio * c)

        self.entryHigh = row['h']#  + (row['h'] * 0.0003)
        self.entryLow = row['l']#  - (row['l'] * 0.0003)


    def trailingStops(self, row):

        if self.openTag != 'Regression Channel' and self.openTag != 'Rejection EMA':

            if self.direction == 'Long':

                #self.trailingStopLoss = self.entryPrice
                self.trailingStopLoss = self.entryPrice + (self.entryPrice * self.backtest.trailingStopRatio)
            
            elif self.direction == 'Short':

                #self.trailingStopLoss = self.entryPrice
                self.trailingStopLoss = self.entryPrice - (self.entryPrice * self.backtest.trailingStopRatio)

        elif self.openTag == 'Regression Channel':


            if self.direction == 'Long':

                #self.trailingStopLoss = self.entryPrice
                self.channelTrailingStopLoss = self.entryPrice + (self.entryPrice * self.backtest.channelTrailingStopRatio)           

            elif self.direction == 'Short':

                #self.trailingStopLoss = self.entryPrice
                self.channelTrailingStopLoss = self.entryPrice - (self.entryPrice * self.backtest.channelTrailingStopRatio)

        elif self.openTag == 'Rejection EMA':

            if self.direction == 'Long':

                #self.trailingStopLoss = self.entryPrice
                self.trailingStopLoss = self.entryPrice + (self.entryPrice * self.backtest.EMAtrailingStopLossRatio)
            
            elif self.direction == 'Short':

                #self.trailingStopLoss = self.entryPrice
                self.trailingStopLoss = self.entryPrice - (self.entryPrice * self.backtest.EMAtrailingStopLossRatio)


    def channelStopAndTakeProfit(self, row):


        self.regressionBeta = row['RegressionBeta' + str(self.backtest.channelPeriod)]

        if self.direction == 'Long':

            self.channelRegressionTakeProfit = (row['RegressionLine' + str(self.backtest.channelPeriod)] + (row['Deviation' + str(self.backtest.channelPeriod)] * self.backtest.channelTrailingDeviation))
            self.channelRegressionStopLoss = (row['RegressionLine' + str(self.backtest.channelPeriod)] - (row['Deviation' + str(self.backtest.channelPeriod)] * self.backtest.channelTrailingDeviation))

        elif self.direction == 'Short':
            self.channelRegressionTakeProfit = (row['RegressionLine' + str(self.backtest.channelPeriod)] - (row['Deviation' + str(self.backtest.channelPeriod)] * self.backtest.channelTrailingDeviation))
            self.channelRegressionStopLoss = (row['RegressionLine' + str(self.backtest.channelPeriod)] + (row['Deviation' + str(self.backtest.channelPeriod)] * self.backtest.channelTrailingDeviation))

               
        c = row['c']

        if self.direction == 'Long':

            self.channelStopLoss = c - (self.backtest.channelStopLossRatio * c)
            self.channelTakeProfit = c + (self.backtest.channelTakeProfitRatio * c)

        elif self.direction == 'Short':

            self.channelStopLoss = c + (self.backtest.channelStopLossRatio * c)
            self.channelTakeProfit = c - (self.backtest.channelTakeProfitRatio * c)

        self.entryHigh = row['h']#  + (row['h'] * 0.0003)
        self.entryLow = row['l']#  - (row['l'] * 0.0003)


    def __str__(self): 

        result = "\n".join([("{}: {}").format(key, self.__dict__[key]) for key, value in sorted(self.__dict__.items())]) 

        return result


    def formatPrint(self):

        pprint.pprint(sorted(self.__dict__.items()))
        print('\n')


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
        self.transactionsDuration = []
        self.transactionPLArray = []
        self.transactionPL100Array = []
        self.transactionPLbyYear = {}
        self.transactionPLbyCurrency = {}
 
    def update(self, instrument, tag, row):           #keeps a backtestRecord for each transaction

        self.transaction['Instrument:               '] = self.backtest.portfolio.openPositions[instrument].instrument
        self.transaction['Entry Time:               '] = self.backtest.portfolio.openPositions[instrument].entryTime
        self.transaction['Entry Price:              '] = self.backtest.portfolio.openPositions[instrument].entryPrice
        self.transaction['Direction:                '] = self.backtest.portfolio.openPositions[instrument].direction
        self.transaction['Duration:                 '] = self.backtest.portfolio.openPositions[instrument].duration
        self.transaction['Number of units:          '] = self.backtest.portfolio.openPositions[instrument].units
        self.transaction['Exit Time:                '] = self.backtest.portfolio.openPositions[instrument].exitTime
        self.transaction['Exit Price:               '] = self.backtest.portfolio.openPositions[instrument].exitPrice
        self.transaction['Transaction $ return:     '] = self.backtest.portfolio.openPositions[instrument].transactionPL
        self.transaction['Transaction % return:     '] = self.backtest.portfolio.openPositions[instrument].transactionPL100
        self.transaction['Portfolio balance:        '] = self.backtest.portfolio.balance
        self.transaction['Reason opened:            '] = self.backtest.portfolio.openPositions[instrument].openTag
        self.transaction['Reason closed:            '] = tag
        self.transaction['Simultaneous positions:   '] = (self.backtest.portfolio.transactionsCurrentlyOpen + 1)
        #self.transaction['Close row: '] = row
        #self.transaction['Open row: '] =
        #self.backtest.portfolio.openPositions[instrument].openRow

        self.log[self.backtest.portfolio.transactions] = dict(self.transaction)  
        self.instrumentLog[(instrument, self.backtest.portfolio.transactions)] = self.log[self.backtest.portfolio.transactions]


        t = self.backtest.portfolio.openPositions[instrument].entryTime.to_pydatetime()

        if str(t.year) in self.transactionPLbyYear.keys():
            self.transactionPLbyYear[str(t.year)] += self.backtest.portfolio.openPositions[instrument].transactionPL         
        else:
            self.transactionPLbyYear[str(t.year)] = self.backtest.portfolio.openPositions[instrument].transactionPL

        if str(instrument) in self.transactionPLbyCurrency.keys():
            self.transactionPLbyCurrency[str(instrument)] += self.backtest.portfolio.openPositions[instrument].transactionPL         
        else:
            self.transactionPLbyCurrency[str(instrument)] = self.backtest.portfolio.openPositions[instrument].transactionPL  

            
        
        #---------builds the array needed for the stats---------#

        self.transactionPLArray.append(self.backtest.portfolio.openPositions[instrument].transactionPL)
        self.transactionPL100Array.append(self.backtest.portfolio.openPositions[instrument].transactionPL100)
        self.transactionsDuration.append(self.backtest.portfolio.openPositions[instrument].duration)
 
    def updateStats(self):      #keeps a backtestRecord for the entire backtest


        self.transactionsDuration = np.array([self.transactionsDuration])
        self.transactionPLArray = np.array([self.transactionPLArray])
        self.transactionPL100Array = np.array([self.transactionPL100Array])
        self.transactionPLArray = np.reshape(self.transactionPLArray, (-1 , 1))

        
       
        self.transactionStats['# of transactions:                '] = self.backtest.portfolio.transactions
        self.transactionStats['# of + transactions:              '] = self.backtest.portfolio.positiveTransactions
        self.transactionStats['# of - transactions:              '] = self.backtest.portfolio.negativeTransactions
        self.transactionStats['# of break even transactions:     '] = self.backtest.portfolio.breakEvenTransactions
        self.transactionStats['Ending balance:                   '] = '{:10,.5f}'.format(self.backtest.portfolio.balance)
        self.transactionStats['Transaction list:                 '] = {key:self.log[key]['Transaction $ return:     '] for key, value in self.log.items()}
        if self.transactionPLArray.size != 0 and self.transactionPL100Array.size != 0:
            self.transactionStats['Mean $ return:                    '] = '{:7,.5f}'.format(np.mean(self.transactionPLArray))
            self.transactionStats['Mean % return:                    '] = '{:7.5f}'.format(np.mean(self.transactionPL100Array))
            self.transactionStats['Mean duration:                    '] = np.mean(self.transactionsDuration)
            self.transactionStats['Std of return:                    '] = '{:7,.5f}'.format(np.std(self.transactionPLArray))
            self.transactionStats['Min return:                       '] = '{:7,.5f}'.format(np.min(self.transactionPLArray))
            self.transactionStats['Max return:                       '] = '{:7,.5f}'.format(np.max(self.transactionPLArray))
            self.transactionStats['Total P&L:                        '] = '{:7,.5f}'.format(np.sum(self.transactionPLArray))
        self.transactionStats['ATR ratio:                        '] = '{:7.5f}'.format(self.backtest.atrRatio)
        self.transactionStats['ADX level below:                  '] = '{:7.5f}'.format(self.backtest.ADXLevelBelow)
        self.transactionStats['ADX level above:                  '] = '{:7.5f}'.format(self.backtest.ADXLevelAbove)
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
        

        self.transactionStats['Channel rolling Correlation:             '] = '{:7.5f}'.format(self.backtest.channelRollingCorrelation)
        self.transactionStats['Channel period:                          '] = '{:7.5f}'.format(self.backtest.channelPeriod)
        self.transactionStats['Channel deviation ratio below:           '] = '{:7.5f}'.format(self.backtest.channelDeviationRatioBelow)
        self.transactionStats['Channel deviation ratio above:           '] = '{:7.5f}'.format(self.backtest.channelDeviationRatioAbove)
        self.transactionStats['Channel stop loss @:                     '] = '{:7.4f}'.format(self.backtest.channelStopLossRatio)
        self.transactionStats['Channel take profit @:                   '] = '{:7.4f}'.format(self.backtest.channelTakeProfitRatio)
        self.transactionStats['Channel trailing stop loss @:            '] = '{:7.4f}'.format(self.backtest.channelTrailingStopRatio)
        self.transactionStats['Channel trailing deviation:              '] = '{:7.4f}'.format(self.backtest.channelTrailingDeviation)

        self.transactionStats['EMA DI level above:                  '] = '{:7.4f}'.format(self.backtest.EMADILevelAbove)
        self.transactionStats['EMA Deviation ratio below:           '] = '{:7.4f}'.format(self.backtest.EMAdeviationRatioBelow)
        self.transactionStats['EMA Deviation ratio above:           '] = '{:7.4f}'.format(self.backtest.EMAdeviationRatioAbove)
        self.transactionStats['EMA ATR ratio:                       '] = '{:7.4f}'.format(self.backtest.EMAatrRatio)
        self.transactionStats['EMA RC close:                        '] = '{:7.5f}'.format(self.backtest.EMArcRatioClose)
        self.transactionStats['EMA RC open:                         '] = '{:7.5f}'.format(self.backtest.EMArcRatioOpen)
        self.transactionStats['EMA RC with direction on close:      '] = '{:7.5f}'.format(self.backtest.EMArcRatioCloseDirection)
        self.transactionStats['EMA RC with direction on open:       '] = '{:7.5f}'.format(self.backtest.EMArcRatioOpenDirection)
        self.transactionStats['EMA stop loss @:                     '] = '{:7.5f}'.format(self.backtest.EMAstopLossRatio)
        self.transactionStats['EMA take profit @:                   '] = '{:7.5f}'.format(self.backtest.EMAtakeProfitRatio)

        self.logStats = dict(self.transactionStats) 
        self.logStatsNoTransactions = dict(self.transactionStats)
        del self.logStatsNoTransactions['Transaction list:                 ']


class portfolio:

    def __init__(self, balance):

        self.balance = balance
        self.startingBalance = balance
        self.transactions = 0
        self.positiveTransactions = 0
        self.negativeTransactions = 0
        self.breakEvenTransactions = 0
        self.transactionsCurrentlyOpen = 0
        self.openPositions = {}
 

    def __str__(self): 

        #result = "\n".join({("{}: {}").format(key, self.__dict__[key]) for
        #key, value in self.__dict__.items()})
        return 'Balance: ' + str(self.balance) + '\n' + \
               'Transactions: ' + str(self.transactions)











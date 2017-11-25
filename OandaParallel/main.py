import pycurl
import json
import pprint
from io import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import indicators
import datetime
import query
from decimal import *



#headersList = ['complete', 'time', 'volume', 'c', 'h', 'l', 'o']
#apiKey = "edae87423ccdc5f4ba01c5480ecb5999-ae8421566f13993d4e667a3551c27385"
#accountNbr = "101-002-4852360-001"




    
class dataObject():

    def __init__(self):

        self.data = None
        self.accountID = None
        self.Query = None

    def dataBuild(self, timeframe, startDate, endDate, offset, *instruments):

        dataDict = {}
        

        for instrument in instruments:  
            
            data = None
            dataConcat = None 
            queryDate = startDate

            while queryDate < endDate:

                print(queryDate , instrument)                                                 
                url         = query.urlparseMethod(timeframe, queryDate, instrument)

                while True:
                    try:
                        dataConcat  = query.instrumentQuery(url)
                    except:
                        print('Handshake failed')                  
                        continue
                    break

                if data is not None:
                    data    = pd.concat([data, dataConcat])
                else:
                    data    = dataConcat
                try: 

                    queryDate   = (dataConcat.index[4999]).to_pydatetime()                 
                    queryDate   = datetime.datetime.combine(queryDate.date(), queryDate.time()) + (datetime.timedelta(minutes=+offset))
                    

                except Exception as e:
                    print(e)
                    print('Repetition failed')
                    break
                
            print(len(data.index))
            dataDict[instrument] = data  

        return dataDict

    def setQuery(self, timeframe, queryDate, instrument):

        self.url = query.urlparseMethod(timeframe, queryDate, instrument)

        return self.url

    def getData(self, url):

        #self.accountID = query.accountID()
        self.data = query.instrumentQuery(url)  

        return self.data

    def setIndicators(self, data, *args):

        self.data = data
        
        for arg in args:
            if arg[0].upper() == 'RSI'.upper():
                y = arg[1]
                (exec('{} = {}.{},{}{}'.format('self.data','indicators', 'RSICust(self.data', y, ')')))

        for arg in args:
            if arg[0].upper() == 'StochRSI'.upper():
                y1, y2, y3 = arg[1], arg[2], arg[3]
                (exec('{} = {}.{},{},{},{}{}'.format('self.data','indicators', 'StochRSICust(self.data', y1, y2, y3, ')')))

        for arg in args:
            if arg[0].upper() == 'EMA'.upper() and arg[1].upper() == 'Price'.upper():
                y1 = arg[2]
                y2 = 'PriceEMA' + str(y1)
                (exec('{} = {}.{},{},{},{}{}'.format('self.data','indicators', 'EMACust(self.data', 'self.data["c"]', y1, repr(y2), ')')))
     
        for arg in args:
            if arg[0].upper() == 'EMA'.upper() and arg[1].upper() == 'Volume'.upper():
                y1 = arg[2]
                y2 = 'VolumeEMA' + str(y1)
                (exec('{} = {}.{},{},{},{}{}'.format('self.data','indicators', 'EMACust(self.data', 'self.data["volume"]', y1, repr(y2), ')')))
        
        for arg in args:
            if arg[0].upper() == 'BearishRC'.upper():
                (exec('{} = {}.{}{}'.format('self.data','indicators', 'bearishRejectionCandle(self.data', ')')))        

        for arg in args:
            if arg[0].upper() == 'BullishRC'.upper():
                (exec('{} = {}.{}{}'.format('self.data','indicators', 'bullishRejectionCandle(self.data',')')))

        for arg in args:
            if arg[0].upper() == 'Highest Price'.upper():
                y = arg[1]
                (exec('{} = {}.{},{}{}'.format('self.data','indicators', 'highestPrice(self.data', y, ')')))

        for arg in args:
            if arg[0].upper() == 'Lowest Price'.upper():
                y = arg[1]
                (exec('{} = {}.{},{}{}'.format('self.data','indicators', 'lowestPrice(self.data', y, ')')))

        for arg in args:
            if arg[0].upper() == 'ADX'.upper():
                y = arg[1]
                (exec('{} = {}.{},{}{}'.format('self.data','indicators', 'ADX(self.data', y, ')')))

        for arg in args:
            if arg[0].upper() == 'Deviation'.upper():
                y = arg[1]
                (exec('{} = {}.{},{}{}'.format('self.data','indicators', 'trailingDeviation(self.data', y, ')')))

        for arg in args:
            if arg[0].upper() == 'Bollinger Bands'.upper():
                y1 = arg[1]
                y2 = arg[2]
                (exec('{} = {}.{},{},{}{}'.format('self.data','indicators', 'bollingerBands(self.data', y1, y2, ')')))

        for arg in args:
            if arg[0].upper() == 'Regression'.upper():
                y1 = arg[1]
                y2 = arg[2]
                (exec('{} = {}.{},{},{}{}'.format('self.data','indicators', 'regression(self.data',y1, y2, ')')))

        for arg in args:
            if arg[0].upper() == 'Gap'.upper():
                y = arg[1]
                (exec('{} = {}.{},{}{}'.format('self.data','indicators', 'gap(self.data', y, ')')))


        return self.data
    

def initialize():

    getcontext().prec = 6

    pd.options.display.float_format = '{:7.5f}'.format
    pd.set_option("display.max_rows",100)
    pd.set_option("display.max_columns",1000)
    pd.set_option('display.max_colwidth',100)

    

    np.set_printoptions(precision=4)
    np.set_printoptions(threshold=np.nan)
    np.set_printoptions(suppress=True)
    

def plotData(data):

    for element in list(data.columns.values):
        #if '_D%' in element:
        #    data[element].plot()
        #if '_k%' in element:
        #    data[element].plot()
        #if 'RSI' in element and not '_k%' in element and not '_D%' in element:
        #    data[element].plot()
        #if 'EMA' in element:
        #    data[element].plot()
        #if 'ADX' in element:
        #    data[element].plot()
        #if 'DI14-' in element:
        #    data[element].plot()
        #if 'DX' in element and not 'ADX' in element:
        #    data[element].plot()
        if '+DI14' in element:
            data[element].plot()

    plt.show()



























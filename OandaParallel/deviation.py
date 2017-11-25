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
import backtest
import conditions





data = pickle.load(open( 'dataSave\\' + '2hoursChannelWithParameters', 'rb'))


for year in range (2007, 2018, 1):

    Total10  = np.array([])
    Total100 = np.array([])
    ATR = np.array([])
    ADX = np.array([])

    for instrument in data.keys():
        #if instrument == 'USD_MXN':
            #print(str(year), ': ', str(instrument))
            #print(data[instrument][str(year)]['ADX14'].mean())
            #print(data[instrument][str(year)]['ATR14'].mean())
            #print(data[instrument][str(year)]['VariationCoefficient10'].mean())
            #print(data[instrument][str(year)]['Deviation10'].mean())
            #print(data[instrument][str(year)]['VariationCoefficient100'].mean())

            Total10 = np.append(Total10, data[instrument][str(year)]['VariationCoefficient10'].mean())
            Total100 = np.append(Total100, data[instrument][str(year)]['VariationCoefficient100'].mean())
            ATR = np.append(ATR, data[instrument][str(year)]['ATR14'].mean())
            ADX = np.append(ADX, data[instrument][str(year)]['ADX14'].mean())

    print(str(year), ' 10:  ', Total10.mean())
    print(str(year), ' 100: ', Total100.mean())
    print(str(year), ' ATR: ', ATR.mean())
    print(str(year), ' ADX: ', ADX.mean())

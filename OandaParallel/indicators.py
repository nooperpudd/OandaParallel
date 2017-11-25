import pandas as pd
import numpy as np
import sys
import math





def RSICust(data, period):

    data['gainLoss'] = data['c'].diff()

    data['gain'] = np.where(data['gainLoss'] > 0, data['gainLoss'], 0)
    data['loss'] = np.where(data['gainLoss'] < 0, data['gainLoss'].abs(), 0)

    smaGain = pd.Series(np.nan)   
    smaLoss = pd.Series(np.nan) 

    smaGain[period] = (data['gain'][1:period+1]).mean()
    smaLoss[period] = (data['loss'][1:period+1]).mean()

    restGain = data['gain'][period+1:]
    restLoss = data['loss'][period+1:]

    data["avgGain"] = pd.concat([smaGain, restGain]).ewm(adjust = False, alpha = (1/period)).mean()
    data["avgLoss"] = pd.concat([smaLoss, restLoss]).ewm(adjust = False, alpha = (1/period)).mean()

    data = data.assign(RS = data["avgGain"] / data["avgLoss"])
    data = data.assign(RSI= 100 - (100 / (1 + data['RS'])))
    data = data.rename(columns={'RSI': 'RSI' + str(period)})
    data.drop(['gainLoss', 'gain', 'loss', 'avgGain', 'avgLoss', 'RS'], axis = 1, inplace=True)

    return data
 

 

def StochRSICust(data, period, fast, slow):

    rsiIn = False
    if not ('RSI' + str(period)) in data.columns:
        data = RSICust(data, period)
        rsiIn = True
 
    data['HighestRSI'] = data[('RSI' + str(period))].rolling(14).max()
    data['LowestRSI'] = data[('RSI' + str(period))].rolling(14).min()

    data = data.assign(StochRSI = ((data[('RSI' + str(period))] - data['LowestRSI']) /(data['HighestRSI'] - data['LowestRSI'])) * 100)
    data = data.rename(columns={'StochRSI': 'StochRSI' + str(period)})

    data[('StochRSI_K' + str(period) + '/' + str(fast))] = data[('StochRSI' + str(period))].rolling(window = fast).mean()
    data[('StochRSI_D' + str(period) + '/' + str(slow))] = data[('StochRSI_K' + str(period) + '/' + str(fast))].rolling(window = slow).mean()

    data.drop(['HighestRSI', 'LowestRSI', ('StochRSI' + str(period))], axis = 1, inplace=True)

    if rsiIn:
        data.drop('RSI' + str(period), axis = 1, inplace=True)
        
    return data


def EMACust(data, column, period, name):
    
    sma = pd.Series(np.nan) 
    sma[period - 1] = (column[0:period]).mean()
    rest = column[period:]
    data[name] = pd.concat([sma, rest]).ewm(adjust = False, span = period).mean()

    return data


def bearishRejectionCandle(data):

    
    data = data.assign(high_low = np.where(((data['h'] - data['l']) != 0), (data['h'] - data['l']), np.NaN))
    data = data.assign(BearishRejectionCandleClose =   ((data['c']  - data['l']) / data['high_low']))
    data = data.assign(BearishRejectionCandleOpen  =   ((data['o']  - data['l']) / data['high_low']))
    
    data.drop('high_low', axis = 1, inplace=True)

    return data


def bullishRejectionCandle(data):

    
    data = data.assign(low_high = np.where(((data['l'] - data['h']) != 0), (data['l'] - data['h']), np.NaN))
    data = data.assign(BullishRejectionCandleClose =   ((data['c']  - data['h']) / data['low_high'])) 
    data = data.assign(BullishRejectionCandleOpen  =   ((data['o']  - data['h']) / data['low_high']))

    
    data.drop('low_high', axis = 1, inplace=True)

    

    return data


def highestPrice(data, period):

    data['HighestPrice' + str(period)] = pd.Series.rolling(data['h'], period).max()

    return data


def lowestPrice(data, period):

    data['LowestPrice' + str(period)] = pd.Series.rolling(data['l'], period).min()

    return data


def trailingDeviation(data, period):


    data[('Deviation' + str(period))]                 =  data['c'].rolling(period).std()
    data[('Mean' + str(period))]                      =  data['c'].rolling(period).mean()


    data = data.assign(VariationCoefficient = (data[('Deviation' + str(period))] / data[('Mean' + str(period))]))
    data = data.rename(columns={'VariationCoefficient': 'VariationCoefficient' + str(period)})

    data = data.assign(DeviationPct = (data[('Deviation' + str(period))] /  data['c']))
    data = data.rename(columns={'DeviationPct': 'Deviation%' + str(period)})

    data = data.assign(HLOverDeviation = ((data['h'] / data['l']) - 1) / data[('Deviation%' + str(period))])
    data = data.rename(columns = {'HLOverDeviation': 'HLOverDeviation' + str(period)})

    data.drop('Mean' + str(period), axis = 1, inplace=True)

    return data


def bollingerBands(data, period, deviation):

    data['bbmean'] =  data['c'].rolling(period).mean()
    data['bbstd']  =  data['c'].rolling(period).std() 
    data[(('UpperBB' + str(period) + '/' + str(deviation)))] = data['bbmean'] + (deviation * data['bbstd'])
    data[(('LowerBB' + str(period) + '/' + str(deviation)))] = data['bbmean'] - (deviation * data['bbstd'])

    data.drop(['bbmean', 'bbstd'], axis = 1, inplace=True)

    return data


def ADX (data, period):

    averageTrueRangeIn = False
    if not ('ATR' + str(period)) in data.columns:
        data = averageTrueRange(data, period)
        averageTrueRangeIn = True

    data['upMove']   = data['h'].diff()
    data['downMove'] = -(data['l'].diff())

    data['+DM'] = np.where(((data['upMove'] > data['downMove']) & (data['upMove'] > 0)), data['upMove'], 0)
    data['-DM'] = np.where(((data['downMove'] > data['upMove']) & (data['downMove'] > 0)), data['downMove'], 0)

    firstDMPlus = pd.Series(np.nan)
    firstDMMinus = pd.Series(np.nan)

    firstDMPlus[period]  = (data['+DM'][1:period+1]).sum()
    firstDMMinus[period] = (data['-DM'][1:period+1]).sum()

    restDMPlus  = data['+DM'][period+1:]
    restDMMinus = data['-DM'][period+1:]
        
    data['+DM' + str(period)] = pd.concat([firstDMPlus, restDMPlus]).ewm(adjust = False, alpha = (1/period)).mean()
    data['-DM' + str(period)] = pd.concat([firstDMMinus, restDMMinus]).ewm(adjust = False, alpha = (1/period)).mean()

    data['+DM' + str(period)] = data['+DM' + str(period)]
    data['-DM' + str(period)] = data['-DM' + str(period)]

    data['+DI' + str(period)] = data['+DM' + str(period)] / data['ATR' + str(period)] * 100
    data['-DI' + str(period)] = data['-DM' + str(period)] / data['ATR' + str(period)] * 100

    data['DX'] = 100 * abs(data['+DI' + str(period)] - data['-DI' + str(period)]) / (data['+DI' + str(period)] + data['-DI' + str(period)])

    firstADX = pd.Series(np.nan)

    firstADX[period]  = (data['DX'][1:period+1]).mean()
    restADX            = data['DX'][period+1:]
 
    data['ADX' + str(period)] = pd.concat([firstADX, restADX]).ewm(adjust = False, alpha = (1/period)).mean()
 
    #data.drop(['+DM' + str(period), '-DM' + str(period), 'DX', '+DM','-DM'], axis = 1, inplace=True)


    return data


def trueRange(data): 

    data['currenHighPreviousClose'] = data['h'] - data['c'].shift(1)
    data['previousCloseCurrentLow'] = data['c'].shift(1) - data['l']
    data['currentHighCurrentLow']   = data['h'] - data['l']

    data['TR'] = data[['currenHighPreviousClose', 'previousCloseCurrentLow', 'currentHighCurrentLow']].max(axis = 1)
    data.drop(['currenHighPreviousClose', 'previousCloseCurrentLow', 'currentHighCurrentLow'], axis = 1, inplace=True)

    return data


def averageTrueRange(data, period): 
    
    data = trueRange(data)

    firstATR          = pd.Series(np.nan)
    firstATR[period]  = (data['TR'][1:period+1]).sum()
    restATR           = data['TR'][period+1:]

    data['ATR' + str(period)] = pd.concat([firstATR, restATR]).ewm(adjust = False, alpha = (1/period)).mean()
    


    data.drop('TR', axis = 1, inplace=True)

    return data


def regression(data, period, deviation):

    
    if not ('Deviation' + str(period)) in data.columns:
        data[('Deviation' + str(period))] = data['c'].rolling(period).std()
        

    def regressionLine(data):

        y = np.array(data)
        x = np.array(range(len(data)))
        M = np.vstack([x, np.ones(len(x))]).T
        b, a = np.linalg.lstsq(M, y)[0]
        line = a + b * x[-1]
        return line

    def regressionBeta(data):

        y = np.array(data)
        x = np.array(range(len(data)))
        M = np.vstack([x, np.ones(len(x))]).T
        b, a = np.linalg.lstsq(M, y)[0]
        line = a + b * x[-1]
        return b


    data['RegressionLine' + str(period)] = data['c'].rolling(window = period).apply(regressionLine)
    data['RegressionBeta' + str(period)] = data['c'].rolling(window = period).apply(regressionBeta)

    data['Range'] = range(len(data.index))
    data['RollingCorrelation' + str(period)]  = data['c'].rolling(window = period).corr(data['Range'])


    data.drop('Range', axis = 1, inplace=True)



    return data


def gap(data, period):

    data['closeMinusOpen'] = data['c'] - data['o'].shift(-1)
    data['gap'] = data['closeMinusOpen'] / data['c']
    data['Gap' + str(period)] = pd.Series.rolling(data['gap'], period).max() 

    data.drop(['gap', 'closeMinusOpen'], axis = 1, inplace=True)

    return data
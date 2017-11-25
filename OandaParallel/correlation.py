import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import pprint
import math


import statsmodels.api as sm
from statsmodels.stats import outliers_influence
import statsmodels.stats.api as sms
from patsy import dmatrices





pd.options.mode.chained_assignment = None 
transactionsData = pickle.load(open('dataSave\\' + 'P&L', 'rb'))


def formatData(transactionsData):

    
    transactionsData['date'] = transactionsData.index.values
    transactionsData.reset_index(drop=True, inplace = True)
    transactionsData = transactionsData.drop('instrument', axis = 1)


    transactionsData.sort_values(by = 'P&L100', inplace = True)

    positiveTransactions = transactionsData[transactionsData['P&L100'] > 0]
    negativeTransactions = transactionsData[transactionsData['P&L100'] < 0]

    transactionsData.sort_values(by = 'Direction', inplace = True)

    longTransactions = transactionsData[transactionsData['Direction'] == 'Long']
    shortTransactions = transactionsData[transactionsData['Direction'] == 'Short']


    positiveTransactions.sort_values(by = 'Direction', inplace = True)
    positiveTransactions.reset_index(drop=True, inplace = True)
    positiveLongTransactions = positiveTransactions[positiveTransactions['Direction'] == 'Long']
    positiveShortTransactions = positiveTransactions[positiveTransactions['Direction'] == 'Short']


    negativeTransactions.sort_values(by = 'Direction', inplace = True)
    negativeTransactions.reset_index(drop=True, inplace = True)
    negativeLongTransactions = negativeTransactions[negativeTransactions['Direction'] == 'Long']
    negativeShortTransactions = negativeTransactions[negativeTransactions['Direction'] == 'Short']


    positiveLongTransactions.set_index(keys = 'date', inplace = True)
    positiveShortTransactions.set_index(keys = 'date', inplace = True)
    negativeLongTransactions.set_index(keys = 'date', inplace = True)
    negativeShortTransactions.set_index(keys = 'date', inplace = True)
    longTransactions.set_index(keys = 'date', inplace = True)
    shortTransactions.set_index(keys = 'date', inplace = True)



    del positiveLongTransactions['Direction']
    del positiveShortTransactions['Direction']
    del negativeLongTransactions['Direction']
    del negativeShortTransactions['Direction']
    del longTransactions['Direction']
    del shortTransactions['Direction']


    positiveLongTransactionsCorrelation = positiveLongTransactions.astype('float64').corr()
    positiveShortTransactionsCorrelation = positiveShortTransactions.astype('float64').corr()
    negativeLongTransactionsCorrelation = negativeLongTransactions.astype('float64').corr()
    negativeShortTransactionsCorrelation = negativeShortTransactions.astype('float64').corr()
    longTransactionsCorrelation = longTransactions.astype('float64').corr()
    shortTransactionsCorrelation = shortTransactions.astype('float64').corr()

    positiveLongTransactionsCorrelationArray = positiveLongTransactionsCorrelation.loc['P&L100']
    positiveShortTransactionsCorrelationArray = positiveShortTransactionsCorrelation.loc['P&L100']
    negativeLongTransactionsCorrelationArray = negativeLongTransactionsCorrelation.loc['P&L100']
    negativeShortTransactionsCorrelationArray = negativeShortTransactionsCorrelation.loc['P&L100']
    longTransactionsCorrelationArray = longTransactionsCorrelation.loc['P&L100']
    shortTransactionsCorrelationArray = shortTransactionsCorrelation.loc['P&L100']


    positiveLongTransactionsCorrelationArray = pd.Series.sort_values(positiveLongTransactionsCorrelationArray, ascending = False)
    positiveShortTransactionsCorrelationArray = pd.Series.sort_values(positiveShortTransactionsCorrelationArray, ascending = False)
    negativeLongTransactionsCorrelationArray = pd.Series.sort_values(negativeLongTransactionsCorrelationArray, ascending = False)
    negativeShortTransactionsCorrelationArray = pd.Series.sort_values(negativeShortTransactionsCorrelationArray, ascending = False)
    longTransactionsCorrelationArray = pd.Series.sort_values(longTransactionsCorrelationArray, ascending = False)   
    shortTransactionsCorrelationArray = pd.Series.sort_values(shortTransactionsCorrelationArray, ascending = False)


    transactions = {}

    transactions['positiveLongTransactionsCorrelationArray'] = positiveLongTransactionsCorrelationArray
    transactions['positiveShortTransactionsCorrelationArray'] = positiveShortTransactionsCorrelationArray
    transactions['negativeLongTransactionsCorrelationArray'] = negativeLongTransactionsCorrelationArray
    transactions['negativeShortTransactionsCorrelationArray'] = negativeShortTransactionsCorrelationArray
    transactions['longTransactionsCorrelationArray'] = longTransactionsCorrelationArray
    transactions['shortTransactionsCorrelationArray'] = shortTransactionsCorrelationArray
    transactions['positiveLongTransactions'] = positiveLongTransactions
    transactions['positiveShortTransactions'] = positiveShortTransactions
    transactions['negativeLongTransactions'] = negativeLongTransactions                                       
    transactions['negativeShortTransactions'] = negativeShortTransactions              
    transactions['longTransactions'] = longTransactions         
    transactions['shortTransactions'] = shortTransactions                     
    transactions['allTransactions'] = transactionsData



    transactions['positiveLongTransactions'].sort_index(inplace = True)
    transactions['positiveShortTransactions'].sort_index(inplace = True)
    transactions['negativeLongTransactions'].sort_index(inplace = True)                                     
    transactions['negativeShortTransactions'].sort_index(inplace = True)
    transactions['longTransactions'].sort_index(inplace = True)
    transactions['shortTransactions'].sort_index(inplace = True)
    transactions['allTransactions'].sort_index(inplace = True)


    return transactions


def plotData(transactions):


    print(transactions['positiveLongTransactionsCorrelationArray'].to_string())
    #print(positiveShortTransactionsCorrelationArray.to_string())

    #print(negativeLongTransactionsCorrelationArray)
    #print(negativeShortTransactionsCorrelationArray)

    #print(longTransactionsCorrelationArray.to_string())
    #print(shortTransactionsCorrelationArray.to_string())


    plt.scatter(transactions['longTransactions'].index.values, transactions['longTransactions']['P&L100'], label = 'Long', color= 'b', alpha = 0.5)
    plt.scatter(transactions['shortTransactions'].index.values, transactions['shortTransactions']['P&L100'], label = 'Short', color= 'r', alpha = 0.5)
    plt.legend()


    plt.figure()
    plt.scatter(transactions['longTransactions']['Deviation%10'], transactions['longTransactions']['P&L100'], label = 'P&L100', alpha = 0.5)
    plt.xlabel('Deviation%10')
    plt.ylabel('P&L100')
    #plt.xlim(xmin=0)
    #plt.ylim(ymin=-0.005)
    plt.title('Long transactions')
    plt.legend()

    plt.figure()
    plt.subplot(211)
    plt.scatter(transactions['positiveLongTransactions']['Deviation%10'], transactions['positiveLongTransactions']['P&L100'], label = 'P&L100', alpha = 0.5)
    plt.xlabel('Deviation%10', labelpad = 5)
    plt.ylabel('P&L100')
    plt.tight_layout(pad=1.0, w_pad=1.0, h_pad=1.0)
    plt.xlim(xmin=0, xmax = 0.01)
    plt.ylim(ymin=-0.005)
    plt.title('Positive long transactions')
    plt.legend()



    plt.subplot(212)
    plt.scatter(transactions['positiveShortTransactions']['Deviation%10'][transactions['positiveShortTransactions']['Deviation%10'] < 0.05], \
                transactions['positiveShortTransactions']['P&L100'][transactions['positiveShortTransactions']['Deviation%10'] < 0.05], label = 'P&L100', alpha = 0.5)
    plt.xlabel('Deviation%10', labelpad = 5)
    plt.ylabel('P&L100')
    plt.tight_layout(pad=1.0, w_pad=1.0, h_pad=1.0)
    plt.xlim(xmin=0, xmax = 0.01)
    plt.ylim(ymin=-0.005)
    plt.title('Positive short transactions')
    plt.legend()

    plt.show()


def statsData(transactions):

    df = transactions['positiveLongTransactions'][['P&L', 'P&L100','Deviation%10', '+DI12', 'ADX12', 'VolumeEMA10']]
    df.rename(columns={'P&L100': 'PL100', 'Deviation%10': 'Deviation10', '+DI12': 'DI12'}, inplace=True)

    for col in  df.columns[:]:
        df[col] = pd.to_numeric(df[col], errors='ignore')


    y, X = dmatrices('PL100 ~ Deviation10', data=df, return_type='dataframe')
    mod = sm.OLS(y, X) 
    res = mod.fit() 
    print(res.summary())


    y, X = dmatrices('PL100 ~ np.log(ADX12)', data=df, return_type='dataframe') # + Deviation10 + np.log(DI12)+ VolumeEMA10'
    mod = sm.OLS(y, X) 
    res = mod.fit() 
    print(res.summary())
    

def toExcel(transactions):

    #transactions['allTransactions'][transactions['allTransactions']['P&L100']
    #< 0].to_excel('dataSave\\' + '-0.00' + '.xlsx')

    return none


def logisticRegression(transactions):

    df = transactions['positiveLongTransactions'][['P&L100','Deviation%10', '+DI12', 'ADX12', 'VolumeEMA10', 'VolumeEMA20']]
    df.rename(columns={'P&L100': 'PL100', 'Deviation%10': 'Deviation10', '+DI12': 'DI12'}, inplace=True)

    for col in  df.columns[:]:
        df[col] = pd.to_numeric(df[col], errors='ignore')


    df['VolumeDiff'] = df['VolumeEMA10'] - df['VolumeEMA20'] 

    df = df.assign(AboveLevel = np.where((df['PL100'] > 0.01), 1, 0))
    df['intercept'] = 1
    train_cols = ['Deviation10', 'VolumeDiff', 'ADX12']


    #df['Deviation10'] = np.log(df['Deviation10'])
    #df['VolumeEMA10'] = np.log(df['VolumeEMA10'])
    #df['ADX12'] = np.log(df['ADX12'])





    print(np.linalg.matrix_rank(df[train_cols].values))
    df.dropna(axis=0, how='any', inplace=True)
    df.reset_index(drop=True, inplace = True)

    #print(df['AboveLevel'].to_string(), df[train_cols].to_string())
    #print(df[train_cols].to_string())




    logit = sm.Logit(df['AboveLevel'], df[train_cols])
    result = logit.fit()
    print(result.summary())
    print(np.exp(result.params))
    


    #df.hist()
    #plt.show()


    



transactions = formatData(transactionsData)

#plotData(transactions)
#statsData(transactions)
#logisticRegression(transactions)






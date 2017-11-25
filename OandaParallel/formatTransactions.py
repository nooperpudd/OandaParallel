import pandas as pd




pd.options.mode.chained_assignment = None 


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


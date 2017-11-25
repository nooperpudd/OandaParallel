import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import pprint
import formatTransactions

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from sklearn.svm import LinearSVR
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.decomposition import PCA

import tensorflow as tf

np.set_printoptions(suppress=True)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)






transactionsData = pickle.load(open('dataSave\\' + 'P&L', 'rb'))





transactions = formatTransactions.formatData(transactionsData)


#pprint.pprint(transactions['allTransactions'])



#------------format data-------------#

def formatLong():

    set = transactions['longTransactions'][['VolumeEMA5','VariationCoefficient10', 'BullishRejectionCandleClose','BullishRejectionCandleOpen','ATR10','+DI14', 'RollingCorrelation20', 'RSI12']]
    #pprint.pprint(list(set.columns.values))
    target = transactions['longTransactions']['P&L100']


    return set, target

def formatShort():

    set = transactions['longTransactions'][['VolumeEMA5','VariationCoefficient10', 'BullishRejectionCandleClose','BullishRejectionCandleOpen','ATR10','+DI14', 'RollingCorrelation20', 'RSI12']]
    #pprint.pprint(list(set.columns.values))
    target = transactions['longTransactions']['P&L100']

    return set, target

def formatAll():


    set = transactions['allTransactions']
    target = transactions['allTransactions']['P&L100']
    set.drop(['P&L', 'P&L100','complete', 'Direction',], axis = 1, inplace = True)
    

    return set, target



set, target = formatAll()





set.reset_index(drop = True, inplace = True)
target.reset_index(drop = True, inplace = True)

l = len(target)
l = int(0.8 * l)
pprint.pprint(len(target))

set = set.apply(pd.to_numeric)
set = set.as_matrix().astype(np.float)
target = np.array(target)



set = np.nan_to_num(set)
set = StandardScaler().fit_transform(set)


pca = PCA(n_components = 2)
pca.fit_transform(set)
print('PCA variance ratio: ', pca.explained_variance_ratio_)


#------------format data-------------#






#predictions = lin_reg.predict(set[60:])

#predictions = np.extract(predictions < 0.20, predictions)
#predictions = np.extract(predictions > -0.20, predictions)
#x = np.linspace(0, predictions.shape[0], num=predictions.shape[0])

#plt.figure()
#plt.scatter(x, predictions)
#plt.ylabel('Return%')
#plt.xlabel('set')
#plt.show()



def classifiers(set, target, l):

    print('\n')
    print('Average returns of target: ', '{:.10f}'.format(np.average(target[l:])))


    #-------------Linear---------------#


    lin_reg = LinearRegression()
    lin_reg.fit(set[:l], target[:l])

    predictionsMSE = lin_reg.predict(set[l:])
    linMSE = mean_squared_error(target[l:], predictionsMSE)
    linMSE = np.sqrt(linMSE)

    print('\n')
    print('Linear Coefficient ', lin_reg.coef_)
    print('Linear average returns: ', '{:.10f}'.format(np.average(predictionsMSE)))
    print('Linear MSE: ', '{:.10f}'.format(linMSE))



    #-------------SVM---------------#


    svm_reg = LinearSVR(epsilon = 0.005)
    svm_reg.fit(set[:l], target[:l])

    svr_predictionsMSE = svm_reg.predict(set[l:])
    svr_MSE = mean_squared_error(target[l:], svr_predictionsMSE)
    svr_MSE = np.sqrt(svr_MSE)

    print('\n')
    print('SVR Coefficient ', svm_reg.coef_)
    print('SVR average returns: ', '{:.10f}'.format(np.average(svr_predictionsMSE)))
    print('SVR MSE: ', '{:.10f}'.format(svr_MSE))




    #-------------SVM poly---------------#


    svm_reg_poly = SVR(kernel = 'poly', degree = 10, C = 10, epsilon = 0.005)
    svm_reg_poly.fit(set[:l], target[:l])

    svr_poly_predictionsMSE = svm_reg_poly.predict(set[l:])
    svr_poly_MSE = mean_squared_error(target[l:], svr_poly_predictionsMSE)
    svr_poly_MSE = np.sqrt(svr_poly_MSE)
    #print('SVR poly Coefficient ', svm_reg_poly.coef_)
    print('\n')
    print('SVR poly average returns: ', '{:.10f}'.format(np.average(svr_poly_predictionsMSE)))
    print('SVR poly MSE: ', '{:.10f}'.format(svr_poly_MSE))



    #-------------Decision tree ---------------#


    tree_reg = DecisionTreeRegressor(max_depth=2, random_state=42)
    tree_reg.fit(set[:l], target[:l])

    tree_reg_predictionsMSE = tree_reg.predict(set[l:])
    tree_reg_MSE = mean_squared_error(target[l:], tree_reg_predictionsMSE)
    tree_reg_MSE = np.sqrt(tree_reg_MSE)

    print('\n')
    print('Decision tree average returns: ', '{:.10f}'.format(np.average(tree_reg_predictionsMSE)))
    print('Decision tree MSE: ', '{:.10f}'.format(tree_reg_MSE))

    #export_graphviz(tree_reg,
    #        out_file=('dataSave\\' + "positive.dot"),
    #        feature_names=['VolumeEMA5','VariationCoefficient10', 'BullishRejectionCandleClose','BullishRejectionCandleOpen','ATR10','+DI14', 'StochRSI_K10/3', 'RollingCorrelation20'],
    #        rounded=True,
    #        filled=True)


    #-------------Gradient Boosting---------------#

    gb_reg = GradientBoostingRegressor(max_depth = 70, n_estimators = 15000, learning_rate = 0.1)
    gb_reg.fit(set[:l], target[:l])
    gb_reg_predictions = gb_reg.predict(set[l:])
    gb_reg_MSE = mean_squared_error(target[l:], gb_reg_predictions)
    gb_reg_MSE = np.sqrt(gb_reg_MSE)

    
    print('\n')
    print('Gradient boosting average returns: ', '{:.10f}'.format(np.average(gb_reg_predictions)))
    print('Gradient boosting MSE: ', '{:.10f}'.format(gb_reg_MSE))
    print('Gradient boosting features importance: ', gb_reg.feature_importances_)
    print('Gradient boosting scores: ', gb_reg.score(set[:l], target[:l]))


        #-------------Boosting---------------#

    ada_reg = AdaBoostRegressor(DecisionTreeRegressor(max_depth=2), n_estimators = 10000, random_state = 42)
    ada_reg.fit(set[:l], target[:l])
    ada_reg_predictions = ada_reg.predict(set[l:])
    ada_reg_MSE = mean_squared_error(target[l:], ada_reg_predictions)
    ada_reg_MSE = np.sqrt(ada_reg_MSE)

    
    print('\n')
    print('Boosting average returns: ', '{:.10f}'.format(np.average(ada_reg_predictions)))
    print('Boosting MSE: ', '{:.10f}'.format(ada_reg_MSE))
    print('Boosting features importance: ', ada_reg.feature_importances_)
    print('Boosting scores: ', ada_reg.score(set[:l], target[:l]))



    
    #-------------Random forest---------------#

    fr_reg = RandomForestRegressor(max_depth=2, n_estimators = 500, max_leaf_nodes = 16, random_state=42, n_jobs=-1)
    fr_reg.fit(set[:l], target[:l])
    fr_reg_predictions = fr_reg.predict(set[l:])
    fr_reg_MSE = mean_squared_error(target[l:], fr_reg_predictions)
    fr_reg_MSE = np.sqrt(fr_reg_MSE)


    print('\n')
    print('Random forest average returns: ', '{:.10f}'.format(np.average(tree_reg_predictionsMSE)))
    print('Random forest MSE: ', '{:.10f}'.format(tree_reg_MSE))
    print('Random forest features importance: ', fr_reg.feature_importances_)
    print('Random forest scores: ', fr_reg.score(set[:l], target[:l]))



    return None


classifiers(set, target, l)
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






def longConditions(self, row, instrument):




        
    if (
        instrument not in self.portfolio.openPositions  or 
       (instrument in self.portfolio.openPositions and self.portfolio.openPositions[instrument].direction != 'Long') and
        self.portfolio.transactionsCurrentlyOpen <= 1 ):
       



        if(
        1 in self.conditionsSet                                                                 and
        row['RollingCorrelation' + str(self.channelPeriod)] > self.channelRollingCorrelation    and
        row['l'] < (row['RegressionLine' + str(self.channelPeriod)] - (row['Deviation' + str(self.channelPeriod)] * self.channelTrailingDeviation)) and
        row['c'] > (row['RegressionLine' + str(self.channelPeriod)] - (row['Deviation' + str(self.channelPeriod)] * self.channelTrailingDeviation)) and
        row['VariationCoefficient10'] < self.channelDeviationRatioBelow                         and
        row['VariationCoefficient10'] > self.channelDeviationRatioAbove                        
        ):  
            self.openTag = 'Regression Channel'
            return True

        elif(
        2 in self.conditionsSet                                             and
        row['l'] == row['LowestPrice3']                                     and
        row['VolumeEMA5'] > row['VolumeEMA20']                              and
        row['VolumeEMA5'] > row['VolumeEMA10']                              and
        #row['RSI7'] < self.RSIOversold                                      and
        row['StochRSI_K10/3'] < self.StochRSIOversold                       and
       (row['h'] - row['l']) >= (row['ATR10'] * self.atrRatio)              and
       (row['h'] - row['l']) <= (row['ATR10'] * 5)                          and 
        row['VariationCoefficient10'] < self.deviationRatioBelow            and 
        row['VariationCoefficient10'] > self.deviationRatioAbove            and
        row['ADX10'] < self.ADXLevelBelow                                   and
        row['ADX10'] > self.ADXLevelAbove                                   and
        row['BullishRejectionCandleClose'] <= self.rcRatioClose             and
        row['BullishRejectionCandleOpen']  <= self.rcRatioOpen                   
        ):
            self.openTag = 'Rejection'
            return True
           

        elif(
        3 in self.conditionsSet                                             and
        row['l'] == row['LowestPrice3']                                     and
        row['VolumeEMA5'] > row['VolumeEMA20']                              and
        row['VolumeEMA5'] > row['VolumeEMA10']                              and
        #row['RSI7'] < self.RSIOversold                                      and
        row['StochRSI_K10/3'] < self.StochRSIOversold                       and
        (row['h'] - row['l']) >= (row['ATR10'] * self.atrRatio)             and
        (row['h'] - row['l']) <= (row['ATR10'] * 5)                         and
        row['VariationCoefficient10'] < self.deviationRatioBelow            and 
        row['VariationCoefficient10'] > self.deviationRatioAbove            and
        row['ADX10'] < self.ADXLevelBelow                                   and
        row['ADX10'] > self.ADXLevelAbove                                   and
        row['BullishRejectionCandleClose'] <= self.rcRatioCloseDirection    and
        row['BullishRejectionCandleOpen']  <= self.rcRatioOpenDirection     and   
        row['c'] > row['o']           
        ):  
            self.openTag = 'Rejection with direction'
            return True

        elif (
        4 in self.conditionsSet                                             and
        row['VolumeEMA5'] > row['VolumeEMA10']                              and
        row['VolumeEMA10'] < row['VolumeEMA20']                             and
        row['StochRSI_K10/3'] < self.StochRSIOversold                       and
       (row['h'] - row['l']) >= (row['ATR10'] * self.atrRatio)              and
       (row['h'] - row['l']) <= (row['ATR10'] * 5)                          and
        row['VariationCoefficient10'] < self.deviationRatioAbove            and
        row['BullishRejectionCandleClose'] <= self.rcRatioClose             and
        row['BullishRejectionCandleOpen']  <= self.rcRatioOpen    
        ):
            self.openTag = 'Rejection Low Volume'
            return True

        elif (
        5 in self.conditionsSet                                             and
        row['VolumeEMA5'] > row['VolumeEMA20']                              and
        row['PriceEMA10'] > row['PriceEMA20']                               and
        row['l'] < row['PriceEMA20']                                        and
        row['c'] > row['PriceEMA10']                                        and
        row['l'] == row['LowestPrice3']                                     and
        row['+DI14'] > self.EMADILevelAbove                                 and
        row['VariationCoefficient10'] < self.EMAdeviationRatioBelow         and 
        row['VariationCoefficient10'] > self.EMAdeviationRatioAbove         and
       (row['h'] - row['l']) >= (row['ATR10'] * self.EMAatrRatio)           and
       (row['h'] - row['l']) <= (row['ATR10'] * 5)                          and
        row['BullishRejectionCandleClose'] <= self.EMArcRatioClose          and
        row['BullishRejectionCandleOpen']  <= self.EMArcRatioOpen                    
        ):
            self.openTag = 'Rejection EMA'
            return True

        elif (
        6 in self.conditionsSet                                             and
        row['VolumeEMA5'] > row['VolumeEMA20']                              and
        row['VolumeEMA5'] > row['VolumeEMA10']                              and
        row['PriceEMA10'] > row['PriceEMA20']                               and
        row['l'] < row['PriceEMA20']                                        and
        row['c'] > row['PriceEMA10']                                        and
        row['l'] == row['LowestPrice3']                                     and
        row['+DI14'] > self.EMADILevelAbove                                 and
        row['VariationCoefficient10'] < self.EMAdeviationRatioBelow         and 
        row['VariationCoefficient10'] > self.EMAdeviationRatioAbove         and
       (row['h'] - row['l']) >= (row['ATR10'] * self.EMAatrRatio)           and
       (row['h'] - row['l']) <= (row['ATR10'] * 5)                          and
        row['BullishRejectionCandleClose'] <= self.EMArcRatioCloseDirection    and
        row['BullishRejectionCandleOpen']  <= self.EMArcRatioOpenDirection     and   
        row['c'] > row['o']                      
        ):
            self.openTag = 'Rejection EMA'
            return True


        


        else:
            return False
    else:
        return False



def closeLongConditions(self, row, instrument): 

    if (



       (    
       (self.portfolio.openPositions[instrument].openTag == 'Rejection' or
        self.portfolio.openPositions[instrument].openTag == 'Rejection with direction') and 
        row['StochRSI_K14/3'] > self.StochRSIOverboughtClose                            #and
        #row['RSI7'] > self.RSIOverboughtClose                        
        ) 
           
        
        or


       (
        row['BearishRejectionCandleClose'] <= self.rcRatioClose                         and
        row['BearishRejectionCandleOpen']  <= self.rcRatioOpen                          and
        (row['h'] - row['l']) >= (row['ATR14'] * self.atrRatio)              
        ) 
        
        or 

        (
        self.portfolio.openPositions[instrument].openTag == 'Rejection EMA'             and
        row['RSI12'] > self.RSIOverboughtClose                        
        ) 
        
       # or
            
       #(
       # self.portfolio.openPositions[instrument].openTag == 'RegressionChannel'         and
       # row['c'] > row['MidUpperRegressionChannel' + str(self.channelPeriod)]
       # )
            

        # or


        #(
        # self.portfolio.openPositions[instrument].direction == 'Long'         and
        # row['h'] > row['UpperBB20/3'] 
        # )    

        ):

        return True
    else:
        return False


     
def shortConditions(self, row, instrument):     





    if (instrument not in self.portfolio.openPositions  or 
       (instrument in self.portfolio.openPositions and self.portfolio.openPositions[instrument].direction != 'Short') and
        self.portfolio.transactionsCurrentlyOpen <= 1 ):

                                                     
        
        if (
        1 in self.conditionsSet                                                                     and
        row['RollingCorrelation' + str(self.channelPeriod)] < -self.channelRollingCorrelation       and
        row['h'] > (row['RegressionLine' + str(self.channelPeriod)] + (row['Deviation' + str(self.channelPeriod)] * self.channelTrailingDeviation)) and
        row['c'] < (row['RegressionLine' + str(self.channelPeriod)] + (row['Deviation' + str(self.channelPeriod)] * self.channelTrailingDeviation)) and
        row['VariationCoefficient10'] < self.channelDeviationRatioBelow                             and
        row['VariationCoefficient10'] > self.channelDeviationRatioAbove                                                      
        ):    

            self.openTag = 'Regression Channel'
            return True

        elif (
        2 in self.conditionsSet                                             and
        row['h'] == row['HighestPrice3']                                    and
        row['VolumeEMA5'] > row['VolumeEMA20']                              and
        row['VolumeEMA5'] > row['VolumeEMA10']                              and
        #row['RSI7'] > self.RSIOverbought                                    and
        row['ADX10'] < self.ADXLevelBelow                                   and
        row['ADX10'] > self.ADXLevelAbove                                   and
        row['StochRSI_K10/3'] > self.StochRSIOverbought                     and
       (row['h'] - row['l']) >= (row['ATR10'] * self.atrRatio)              and
       (row['h'] - row['l']) <= (row['ATR10'] * 5)                          and 
        row['VariationCoefficient10'] < self.deviationRatioBelow            and 
        row['VariationCoefficient10'] > self.deviationRatioAbove            and
        row['BearishRejectionCandleClose'] <= self.rcRatioClose             and
        row['BearishRejectionCandleOpen']  <= self.rcRatioOpen                       
        ):
            self.openTag = 'Rejection'
            return True
            
        

        elif (
        3 in self.conditionsSet                                             and
        row['h'] == row['HighestPrice3']                                    and
        row['VolumeEMA5'] > row['VolumeEMA20']                              and
        row['VolumeEMA5'] > row['VolumeEMA10']                              and
        #row['RSI7'] > self.RSIOverbought                                    and
        row['ADX10'] < self.ADXLevelBelow                                   and
        row['ADX10'] > self.ADXLevelAbove                                   and
        row['StochRSI_K10/3'] > self.StochRSIOverbought                     and
       (row['h'] - row['l']) >= (row['ATR10'] * self.atrRatio)              and
       (row['h'] - row['l']) <= (row['ATR10'] * 5)                          and             
        row['VariationCoefficient10'] < self.deviationRatioBelow            and 
        row['VariationCoefficient10'] > self.deviationRatioAbove            and
        row['BearishRejectionCandleClose'] <= self.rcRatioCloseDirection    and
        row['BearishRejectionCandleOpen']  <= self.rcRatioOpenDirection     and    
        row['c'] < row['o']             
        ):    
            self.openTag = 'Rejection with direction'
            return True

        elif (
        4 in self.conditionsSet                                             and
        row['VolumeEMA5'] > row['VolumeEMA10']                              and
        row['VolumeEMA10'] < row['VolumeEMA20']                             and
        row['StochRSI_K10/3'] > self.StochRSIOverbought                     and
       (row['h'] - row['l']) >= (row['ATR10'] * self.atrRatio)              and
       (row['h'] - row['l']) <= (row['ATR10'] * 5)                          and
        row['VariationCoefficient10'] < self.deviationRatioAbove            and
        row['BearishRejectionCandleClose'] <= self.rcRatioClose             and
        row['BearishRejectionCandleOpen']  <= self.rcRatioOpen                       
        ):
            self.openTag = 'Rejection Low Volume'
            return True

        elif (
        5 in self.conditionsSet                                             and
        row['VolumeEMA5'] > row['VolumeEMA20']                              and
        row['PriceEMA10'] < row['PriceEMA20']                               and
        row['c'] < row['PriceEMA10']                                        and
        row['h'] > row['PriceEMA20']                                        and
        row['h'] == row['HighestPrice3']                                    and
        row['VariationCoefficient10'] < self.EMAdeviationRatioBelow         and 
        row['VariationCoefficient10'] > self.EMAdeviationRatioAbove         and
        row['-DI14'] > self.EMADILevelAbove                                 and
       (row['h'] - row['l']) >= (row['ATR10'] * self.EMAatrRatio)           and
       (row['h'] - row['l']) <= (row['ATR10'] * 5)                          and
        row['BearishRejectionCandleClose'] <= self.EMArcRatioClose          and
        row['BearishRejectionCandleOpen']  <= self.EMArcRatioOpen                       
        ):
            self.openTag = 'Rejection EMA'
            return True

        elif (
        6 in self.conditionsSet                                             and
        row['VolumeEMA5'] > row['VolumeEMA20']                              and
        row['VolumeEMA5'] > row['VolumeEMA10']                              and
        row['PriceEMA10'] < row['PriceEMA20']                               and
        row['c'] < row['PriceEMA10']                                        and
        row['h'] > row['PriceEMA20']                                        and
        row['h'] == row['HighestPrice3']                                    and
        row['VariationCoefficient10'] < self.EMAdeviationRatioBelow         and 
        row['VariationCoefficient10'] > self.EMAdeviationRatioAbove         and
        row['-DI14'] > self.EMADILevelAbove                                 and
       (row['h'] - row['l']) >= (row['ATR10'] * self.EMAatrRatio)           and
       (row['h'] - row['l']) <= (row['ATR10'] * 5)                          and
        row['BearishRejectionCandleClose'] <= self.EMArcRatioCloseDirection and
        row['BearishRejectionCandleOpen']  <= self.EMArcRatioOpenDirection  and    
        row['c'] < row['o']                           
        ):
            self.openTag = 'Rejection EMA'
            return True



        


        else:
            return False
    else:
         return False



def closeShortConditions(self, row, instrument):

    if (
       (
       (self.portfolio.openPositions[instrument].openTag == 'Rejection' or
        self.portfolio.openPositions[instrument].openTag == 'Rejection with direction') and 
        row['StochRSI_K14/3'] < self.StochRSIOversoldClose            #and
        #row['RSI7'] < self.RSIOversoldClose
       
        )
            
        or
            
       (
        row['BullishRejectionCandleClose'] <= self.rcRatioClose       and
        row['BullishRejectionCandleOpen']  <= self.rcRatioOpen        and
        (row['h'] - row['l']) >= (row['ATR14'] * self.atrRatio)        
        )

        or

       (
        self.portfolio.openPositions[instrument].openTag == 'Rejection EMA'  and 
        row['RSI12'] < self.RSIOversoldClose
        )



       # or
            
       #(
       # self.portfolio.openPositions[instrument].openTag == 'Regression Channel'         and
       # row['c'] < row['MidLowerRegressionChannel' + str(self.channelPeriod)]
       # )

        #  or
            
        #(
        # self.portfolio.openPositions[instrument].direction == 'Short' and
        # row['l'] < row['LowerBB20/3']      
        # )
            

        ):
        return True
    else:
        return False
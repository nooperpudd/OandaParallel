import pycurl
import json
import pprint
from io import *
import pandas as pd
import numpy as np
import datetime
import time
import urllib.request
import urllib.parse



#2015-10-21 04:30:00


def urlparseMethod(timeframe, queryDate, instrument):

   

    scheme  = 'https'
    netloc  = 'api-fxpractice.oanda.com'
    params  = ''
    query   = 'count=500&price=M&granularity=M15'
    fragment = ''


    #-------path data----------#

    
    #path    = '/v3/instruments/AUD_NZD/candles'

    target    = 'instruments'      #instruments or accounts  
    specifics = instrument          #intrument or accoundID
    function  = 'candles'

    pathItems = {'base'         : '/v3',
                 'target'       : target,
                 'specifics'    : specifics,
                 'function'     : function
                 }

    path = '/'.join([v for k, v in pathItems.items()])    

      


    def setQueryItems(timeframe, queryDate):
        
        if queryDate == None:
            unixtime = None           
        else:
            unixtime = time.mktime(queryDate.timetuple())


        #-------query data---------#

        count       = 5000
        price       = 'M'
        granularity = timeframe
        alignmentTimezone = 'America/New_York'
        dailyAlignment = 17


        if unixtime == None:

            queryItems   = {'count'             : count,
                            'price'             : price,
                            'granularity'       : granularity,
                            'alignmentTimezone' : alignmentTimezone}
        else:

            queryItems   = {'count'             : count,
                            'price'             : price,
                            'granularity'       : granularity,
                            'alignmentTimezone' : alignmentTimezone,
                            'dailyAlignment'    : dailyAlignment,
                            'from'              : unixtime}
    
        return queryItems


    queryItems = setQueryItems(timeframe, queryDate)     
    queryItems = ['{}={}'.format(k,v) for k,v in queryItems.items()]
    query = '&'.join(queryItems)


    #-------assemble---------#

    urlData = {'scheme'  : scheme, 
               'netloc'  : netloc, 
               'path'    : path, 
               'params'  : params, 
               'query'   : query, 
               'fragment': fragment}




    urlParsed = urllib.parse.ParseResult(**urlData)
    urlFinal = urllib.parse.urlunparse(urlParsed)

    return urlFinal

def accountID():

    headers = ["Content-Type: application/json", "Authorization: Bearer edae87423ccdc5f4ba01c5480ecb5999-ae8421566f13993d4e667a3551c27385"]
    body = BytesIO()
    header = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, "https://api-fxpractice.oanda.com/v3/accounts")
    c.setopt(c.HTTPHEADER, headers)
    c.setopt(c.WRITEFUNCTION, body.write)
    c.setopt(c.HEADERFUNCTION, header.write )
    c.perform()


    bodyContent = json.loads(body.getvalue())
    #print(json.dumps(bodyContent, indent=1))
    #pprint.pprint(bodyContent['accounts'][0]['id'])

    return None

def instrumentQuery(url):

    #url = urlparseMethod()
    headers = ["Content-Type: application/json", "Authorization: Bearer edae87423ccdc5f4ba01c5480ecb5999-ae8421566f13993d4e667a3551c27385"]
    body = BytesIO()
    header = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.HTTPHEADER, headers)
    c.setopt(c.WRITEFUNCTION, body.write)
    c.setopt(c.HEADERFUNCTION, header.write )
    c.perform()


    #----------------converts body to a dataframe---------------------#

    bodyContent = json.loads(body.getvalue())
    #pprint.pprint(bodyContent)
    candle = pd.DataFrame(bodyContent['candles'])
    mid = pd.DataFrame.from_records(candle['mid'])
    candle.drop('mid', axis=1, inplace = True)
    candle = pd.concat([candle, mid], axis=1)

    candle['o']    = pd.to_numeric(candle['o'])
    candle['h']    = pd.to_numeric(candle['h'])
    candle['l']    = pd.to_numeric(candle['l'])
    candle['c']    = pd.to_numeric(candle['c'])
    candle['time'] = pd.to_datetime(candle['time'])
    candle['time'] = candle['time'] - datetime.timedelta(hours=4)
    candle.set_index('time', inplace = True)
    

   #----------------converts body to a dataframe---------------------#
   
    #curve.plot()
    #plt.show()


    return candle

def generic(**kargs):


    headers = ["Content-Type: application/json", "Authorization: Bearer edae87423ccdc5f4ba01c5480ecb5999-ae8421566f13993d4e667a3551c27385"]
    body = BytesIO()
    header = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, "https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles?count=500&price=M&granularity=M15")
    c.setopt(c.HTTPHEADER, headers)
    c.setopt(c.WRITEFUNCTION, body.write)
    c.setopt(c.HEADERFUNCTION, header.write )
    c.perform()

    return header, body





#S5 	5 second candlesticks, minute alignment
#S10 	10 second candlesticks, minute alignment
#S15 	15 second candlesticks, minute alignment
#S30 	30 second candlesticks, minute alignment
#M1 	1 minute candlesticks, minute alignment
#M2 	2 minute candlesticks, hour alignment
#M4 	4 minute candlesticks, hour alignment
#M5 	5 minute candlesticks, hour alignment
#M10 	10 minute candlesticks, hour alignment
#M15 	15 minute candlesticks, hour alignment
#M30 	30 minute candlesticks, hour alignment
#H1 	1 hour candlesticks, hour alignment
#H2 	2 hour candlesticks, day alignment
#H3 	3 hour candlesticks, day alignment
#H4 	4 hour candlesticks, day alignment
#H6 	6 hour candlesticks, day alignment
#H8 	8 hour candlesticks, day alignment
#H12 	12 hour candlesticks, day alignment
#D 	1 day candlesticks, day alignment
#W 	1 week candlesticks, aligned to start of week
#M 	1 month candlesticks, aligned to first day of the month
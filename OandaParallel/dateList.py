from datetime import datetime, timedelta
import pprint

import pandas as pd


def make15Minutes(startDate, endDate):

    d1 = startDate
    d2 = endDate

    delta = d2 - d1

    def addTimeDelta(i):
        return pd.Timestamp(d1 + timedelta(seconds=(i * 900)))

    x = list(map(addTimeDelta, range((delta.days*96) + 1)))

    return x


def make1Hour(startDate, endDate):

    d1 = startDate
    d2 = endDate

    delta = d2 - d1

    def addTimeDelta(i):
        return pd.Timestamp(d1 + timedelta(seconds=(i * 3600)))

    x = list(map(addTimeDelta, range((delta.days*24) + 1)))

    return x


def make2Hours(startDate, endDate):

    d1 = startDate
    d2 = endDate

    delta = d2 - d1

    def addTimeDelta(i):
        return pd.Timestamp(d1 + timedelta(seconds=(i * 7200)))

    x = list(map(addTimeDelta, range((delta.days*12) + 1)))
    

    return x


def makeDays(startDate, endDate):

    d1 = startDate.date()
    d2 = endDate.date()

    delta = d2 - d1

    def addTimeDelta(i):
        return d1 + timedelta(days=(i))

    x = list(map(lambda i: addTimeDelta(i), range((delta.days) + 1)))
    #x = list(filter(lambda i: i.weekday() not in [5], x))

    return x

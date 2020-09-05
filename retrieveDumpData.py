import pandas_datareader.data as pddata
import datetime
import numpy as np

def oneYearDump(ticker, fileName, startDate=datetime.date.today() - datetime.timedelta(days=365), endDate=datetime.date.today()):
    """
    Utilizing other methods within the modules (retrieveData, calcReturn, dumpData) to quickly retrieve, calculate return and dump data (pickle).

    Limitations:
        --Data is defaulted to "av-daily-adjusted" from Alpha Advantage
        --No means to change the return column name as well as the name of column to perform the calculation on
    """
    dataFrame = retrieveData(ticker, startDate=startDate, endDate=endDate)
    df = calcReturn(dataFrame,ticker=ticker)
    dumpData(df,fileName)

def oneYearDump_logRet(ticker, fileName, startDate=datetime.date.today() - datetime.timedelta(days=365), endDate=datetime.date.today()):
    """
    Utilizing other methods within the modules (retrieveData, calcReturn, dumpData) to quickly retrieve, calculate return and dump data (pickle).
    Use log return instead of normal return

    Limitations:
        --Data is defaulted to "av-daily-adjusted" from Alpha Advantage
        --No means to change the return column name as well as the name of column to perform the calculation on
    """
    try:
        print('Attempting to download data for: ' + ticker)
        dataFrame = retrieveData(ticker, startDate=startDate, endDate=endDate)
        dataFrame.loc[abs(dataFrame['adjusted close'] / dataFrame['close']) > 1.5, 'adjusted close'] = dataFrame['close']
        df = calcReturn_log(dataFrame,ticker=ticker)
        dumpData(df,fileName)
    except ValueError:
        print('Cannot download' + ticker + ' data...')


def retrieveData(ticker, startDate=datetime.date.today() - datetime.timedelta(days=365), endDate=datetime.date.today(), apiKey='QSMUWQIPLV31UH4Y',dataSource='av-daily-adjusted'):
    """
    Method to retrieve data from Alpha Advantage as a pandas dataframe, need a free API key.
    Params:
    ticker : str
        ticker symbol of stock, ETFs, mutual funds, etc.
    startDate: datetime
        start date for query, default to one year ago from today
    endDate: datetime
        end date for query, default to today
    apiKey : str
        free API key from Alpha Advantage
    endpints: str
        type of data i.e. av-intraday, av-daily, av-daily-adjusted, av-weekly, av-weekly-adjusted, av-monthly, av-monthly-adjsuted
        default to av-daily-adjusted
    """
    df = pddata.DataReader(name=ticker, data_source=dataSource, start=startDate, end=endDate, api_key=apiKey)
    return df

def calcReturn_log(df,col='adjusted close', returnCol='Ret',reverse=False,ticker=''):
    """
    Method to calculate log return
    df : pandas dataframe
        ideally from the retrieveData method but could from any where
    col : str
        column to calculate return from i.e. closing price, adjusted close...
        default to 'adjusted close' based on current Alpha Advantage returned data set
    retrunCol : str
        name of the newly calculated returns column
        default to 'Ret'
    reverse : boolean
        default to False to signify ascending date, set to True if decending
    """
    returnCol = ticker + '_Ret' if ticker != '' else returnCol
    if reverse==False:
        _tmp = np.log(df[col][1:].to_numpy()/df[col][:-1].to_numpy())
        df[returnCol] = np.append(_tmp, np.array([0.]))
    else:
        _tmp = np.log(df[col][:-1].to_numpy()/df[col][1:].to_numpy())
        df[returnCol]= np.append(np.array([0.], _tmp))
    return df

def calcReturn(df,col='adjusted close', returnCol='Ret',reverse=False,ticker=''):
    """
    Method to calculate return
    df : pandas dataframe
        ideally from the retrieveData method but could from any where
    col : str
        column to calculate return from i.e. closing price, adjusted close...
        default to 'adjusted close' based on current Alpha Advantage returned data set
    retrunCol : str
        name of the newly calculated returns column
        default to 'Ret'
    reverse : boolean
        default to False to signify ascending date, set to True if decending
    """
    returnCol = ticker + '_Ret' if ticker != '' else returnCol
    if reverse==False:
        df[returnCol]= df[col].diff()/df[col].shift(1)
    else:
        df[returnCol]= df[col].diff()/df[col].shift(-1)
    return df

def dumpData(df, name):
    """
    Dump data to a pickle file
    df : pandas dataframe
    name : str
        pickle file name
    """
    df.to_pickle(name)
import pandas_datareader.data as pddata

def get_sector_perf(apiKey):
    """
    Wrapper to retrieve sector performance from Alpha Advantage with a default API Key
    """
    api_key ='QSMUWQIPLV31UH4Y' if apiKey =='' else apiKey
    df = pddata.get_sector_performance_av(api_key)
    return df
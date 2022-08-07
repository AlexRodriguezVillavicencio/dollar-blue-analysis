def variation(serie):
    return serie.pct_change()
    
def volatility(variation):
    return variation.rolling(40).std()*100*(260)**0.5

def gap(df):
    return ((df['usd_blue']/df['usd_official']) -1)*100
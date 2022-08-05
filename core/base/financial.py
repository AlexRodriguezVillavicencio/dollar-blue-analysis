def variation(df):
    return df['v'].pct_change()
    
def volatility(variation):
    return variation.rolling(40).std()*100*(260)**0.5

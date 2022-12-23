import pandas as pd

def na_seadec(x: pd.Series, period: int=13, method: str="linear") -> pd.Series:
    trend = x.rolling(window=period, min_periods=1, center=True).mean()
    detrend = x - trend
    
    monthly_mean = detrend.groupby(detrend.index.month).mean()
    
    anomalies = detrend.copy()
    months = anomalies.index.month

    for i, v in zip(monthly_mean.index, monthly_mean):
        anomalies[months == i] = anomalies[months == i] - v

    anomalies = anomalies.interpolate(method=method)

    for i, v in zip(monthly_mean.index, monthly_mean):
        anomalies[months == i] = anomalies[months == i] + v
    
    anomalies = anomalies + trend

    return anomalies
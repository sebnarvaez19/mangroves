import pandas as pd

def na_seadec(x: pd.Series, period: int=13, method: str="linear") -> pd.Series:
    """
    Function to interpolate the NaN values in a series but without affect
    the long term trend and the seasonal component.

    This function decompose the time series and interpolate the anomalies with
    the interpolation method selectd by he user.

    This function was made based on ImputeTS function for R with the same 
    name: https://github.com/SteffenMoritz/imputeTS/

    Parameters
    ----------
    x : pd.Series
        Series of interest with the NaN values.

    period : int
        Period of the time series to calculate the long term trend.

    method : str
        Method of interpolation to fill the NaN values in the anomalies.
        the full list of option coul be found in pandas.Series.interpolate()
        method: https://pandas.pydata.org/docs/reference/api/pandas.Series.interpolate.html

    Returns
    -------
    anomalies : pd.Series
        Series interpolated.
    """

    # Get the long term trend with a rolling mean
    trend = x.rolling(window=period, min_periods=1, center=True).mean()
    
    # Remove the trend
    detrend = x - trend
    
    # Calculate the seasonal component with a mean by month
    monthly_mean = detrend.groupby(detrend.index.month).mean()
    
    # Create the anomalies series
    anomalies = detrend.copy()

    # Extract the months from the series
    months = anomalies.index.month

    # Iterate over the months and motlhy mean data and remove it
    # from detrended data
    for i, v in zip(monthly_mean.index, monthly_mean):
        anomalies[months == i] = anomalies[months == i] - v

    # Interpolate anomalies
    anomalies = anomalies.interpolate(method=method)

    # Restore de seasonal component
    for i, v in zip(monthly_mean.index, monthly_mean):
        anomalies[months == i] = anomalies[months == i] + v
    
    # Restore the long term trend
    anomalies = anomalies + trend

    return anomalies
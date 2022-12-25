import numpy as np
import pandas as pd

from statsmodels.tsa.seasonal import seasonal_decompose

def na_seadec(x: pd.Series, method: str="linear", model: str="additive") -> pd.Series:
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

    method : str
        Method of interpolation to fill the NaN values in the anomalies.
        the full list of option coul be found in pandas.Series.interpolate()
        method: 
        https://pandas.pydata.org/docs/reference/api/pandas.Series.interpolate.html

    model : str
        Additive or Multiplicative. The kind of model to decompose the 
        time series. To read more about the difference between the two models
        could be found in statsmodels.tsa.seasonal.seasonal_decompose()
        function documentation:
        https://www.statsmodels.org/dev/generated/statsmodels.tsa.seasonal.seasonal_decompose.html

    Returns
    -------
    anomalies : pd.Series
        Series interpolated.
    """

    # Get the time to reconstruct the series
    time = x.index

    # Find the NaN values
    mask = x.isna()

    # Interpolate the original series
    interpolated = x.interpolate(method=method)

    # Decompose the series with seasonal_decompose from statsmodels
    components = seasonal_decompose(interpolated, model=model, extrapolate_trend="freq")

    # Sum the trend with the residuals to get the series without 
    # seasonality
    ts_no_seasonal = components.trend + components.resid

    # Restor the NaN values
    ts_no_seasonal[mask] = np.nan

    # Create the second series to interpolate data without seasonality
    x2 = pd.Series(data=ts_no_seasonal, index=time)

    # Interpolate TS without seasonality
    x2 = x2.interpolate(method=method)

    # Add the seasonality to the interpolated data
    x2 = x2 + components.seasonal

    # Fill the NaN with the interpolated data
    x[mask] = x2[mask]

    return x

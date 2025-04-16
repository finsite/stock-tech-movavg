"""Module for calculating different types of moving averages.
"""

import numpy as np
import pandas as pd


def calculate_moving_average(data: pd.Series, window: int, method: str = "sma") -> pd.Series:
    """Calculate a specified moving average type.

    :param data: Pandas Series of stock prices
    :param window: Window size for the moving average
    :param method: Type of moving average ('sma', 'ema', 'wma', 'hma')
    :return: Pandas Series containing moving average values
    """
    if method == "sma":
        return data.rolling(window=window).mean()
    elif method == "ema":
        return data.ewm(span=window, adjust=False).mean()
    elif method == "wma":
        weights = np.arange(1, window + 1)
        return data.rolling(window).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)
    elif method == "hma":
        half_length = int(window / 2)
        sqrt_length = int(np.sqrt(window))
        wma_half = calculate_moving_average(data, half_length, "wma")
        wma_full = calculate_moving_average(data, window, "wma")
        diff_wma = 2 * wma_half - wma_full
        return calculate_moving_average(diff_wma, sqrt_length, "wma")
    else:
        raise ValueError("Invalid method. Choose from 'sma', 'ema', 'wma', or 'hma'.")

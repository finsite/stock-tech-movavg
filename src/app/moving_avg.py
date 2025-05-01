"""
Module for calculating different types of moving averages.

This module contains functions to compute moving averages from a given pandas Series.
Supported methods:
- Simple Moving Average (SMA)
- Exponential Moving Average (EMA)
- Weighted Moving Average (WMA)
- Hull Moving Average (HMA)
"""

from typing import Literal

import numpy as np
import pandas as pd

from app.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)


def calculate_moving_average(
    data: pd.Series,
    window: int,
    method: Literal["sma", "ema", "wma", "hma"] = "sma",
) -> pd.Series:
    """
    Compute a moving average of the specified type.

    Args:
    ----
        data (pd.Series): Time series of stock prices.
        window (int): Number of periods to include in the moving average.
        method (Literal): Moving average type ('sma', 'ema', 'wma', 'hma').

    Returns:
    -------
        pd.Series: Calculated moving average series.

    Raises:
    ------
        ValueError: If the method is not one of the supported types.
    """
    logger.info(f"Calculating {method.upper()} with window={window}")

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

    raise ValueError("Invalid method. Choose from 'sma', 'ema', 'wma', or 'hma'.")

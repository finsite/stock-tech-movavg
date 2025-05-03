"""Module for calculating various types of moving averages."""

from typing import Literal, Union

import numpy as np
import pandas as pd
from pandas import Series

from app.logger import setup_logger

logger = setup_logger(__name__)

MovingAverageMethod = Literal["sma", "ema", "wma", "hma", "vwap", "dema", "tema", "kama", "tma"]


def calculate_moving_average(
    data: Series,
    window: int,
    method: MovingAverageMethod = "sma",
    volume: Series | None = None,
) -> Series:
    """Compute a moving average of the specified type."""
    logger.info(f"Calculating {method.upper()} with window={window}")

    if method == "sma":
        result = data.rolling(window=window).mean()
        return pd.Series(result, index=data.index)

    if method == "ema":
        result = data.ewm(span=window, adjust=False).mean()
        return pd.Series(result, index=data.index)

    if method == "wma":
        weights = np.arange(1, window + 1)

        def weighted_avg(x: np.ndarray) -> float:
            return float(np.dot(x, weights) / weights.sum())

        result = data.rolling(window).apply(weighted_avg, raw=True)
        return pd.Series(result, index=data.index)

    if method == "hma":
        half_length = max(1, int(window / 2))
        sqrt_length = max(1, int(np.sqrt(window)))
        wma_half = calculate_moving_average(data, half_length, "wma")
        wma_full = calculate_moving_average(data, window, "wma")
        diff = 2 * wma_half - wma_full
        return calculate_moving_average(diff, sqrt_length, "wma")

    if method == "vwap":
        if volume is None:
            raise ValueError("VWAP requires volume data.")
        cum_pv = (data * volume).cumsum()
        cum_vol = volume.cumsum().replace(0, np.nan)
        return pd.Series(cum_pv / cum_vol, index=data.index)

    if method == "dema":
        ema = calculate_moving_average(data, window, "ema")
        ema2 = calculate_moving_average(ema, window, "ema")
        return 2 * ema - ema2

    if method == "tema":
        ema1 = calculate_moving_average(data, window, "ema")
        ema2 = calculate_moving_average(ema1, window, "ema")
        ema3 = calculate_moving_average(ema2, window, "ema")
        return 3 * (ema1 - ema2) + ema3

    if method == "kama":
        change = (data - data.shift(window)).abs()
        volatility = data.diff().abs().rolling(window=window).sum()

        # Ensure both are Series to allow `.replace()`
        change = pd.Series(change, index=data.index)
        volatility = pd.Series(volatility, index=data.index).replace(0, np.nan)

        er = change / volatility
        fast = 2 / (2 + 1)
        slow = 2 / (30 + 1)
        sc = (er * (fast - slow) + slow) ** 2

        kama = data.copy().astype("float64")
        kama.iloc[:window] = data.iloc[:window]

        for i in range(window, len(data)):
            kama.iloc[i] = kama.iloc[i - 1] + sc.iloc[i] * (data.iloc[i] - kama.iloc[i - 1])

        return pd.Series(kama, index=data.index)

    elif method == "tma":
        sma1 = data.rolling(window=window).mean()
        sma1 = pd.Series(sma1, index=data.index)  # Ensure it's a Series
        return pd.Series(sma1.rolling(window=window).mean(), index=data.index)

    raise ValueError(
        "Invalid method. Choose from 'sma', 'ema', 'wma', 'hma', 'vwap', 'dema', 'tema', 'kama', 'tma'."
    )

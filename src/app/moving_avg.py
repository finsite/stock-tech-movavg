"""Module for calculating various types of moving averages."""

from typing import Literal, cast

import numpy as np
import pandas as pd
from pandas import Series

from app.logger import setup_logger

logger = setup_logger(__name__)

MovingAvgMethod = Literal["sma", "ema", "wma", "hma", "vwap", "dema", "tema", "kama", "tma"]


def calculate_moving_average(
    data: Series,
    window: int,
    method: MovingAvgMethod = "sma",
    volume: Series | None = None,
) -> Series:
    """Compute a moving average of the specified type."""
    logger.info(f"Calculating {method.upper()} with window={window}")

    if method == "sma":
        return cast(Series, data.rolling(window=window).mean())

    elif method == "ema":
        return cast(Series, data.ewm(span=window, adjust=False).mean())

    elif method == "wma":
        weights = np.arange(1, window + 1)
        result = data.rolling(window).apply(
            lambda x: np.dot(x.values, weights) / weights.sum(), raw=False
        )
        return cast(Series, result)

    elif method == "hma":
        half_length = max(1, int(window / 2))
        sqrt_length = max(1, int(np.sqrt(window)))
        wma_half = calculate_moving_average(data, half_length, "wma")
        wma_full = calculate_moving_average(data, window, "wma")
        diff_wma = 2 * wma_half - wma_full
        return calculate_moving_average(diff_wma, sqrt_length, "wma")

    elif method == "vwap":
        if volume is None:
            raise ValueError("VWAP requires volume data.")
        cum_pv = (data * volume).cumsum()
        cum_vol = volume.cumsum()
        return cast(Series, cum_pv / cum_vol)

    elif method == "dema":
        ema = calculate_moving_average(data, window, "ema")
        ema_of_ema = calculate_moving_average(ema, window, "ema")
        return 2 * ema - ema_of_ema

    elif method == "tema":
        ema1 = calculate_moving_average(data, window, "ema")
        ema2 = calculate_moving_average(ema1, window, "ema")
        ema3 = calculate_moving_average(ema2, window, "ema")
        return 3 * (ema1 - ema2) + ema3

    elif method == "kama":
        change = (data - data.shift(window)).abs()
        volatility = data.diff().abs().rolling(window=window).sum()
        if not isinstance(volatility, pd.Series):
            volatility = pd.Series(volatility, index=data.index)
        volatility = volatility.replace(0, 1)
        er = change / volatility
        fast = 2 / (2 + 1)
        slow = 2 / (30 + 1)
        sc = (er * (fast - slow) + slow) ** 2
        kama = data.copy()
        kama.iloc[:window] = data.iloc[:window]
        for i in range(window, len(data)):
            kama.iloc[i] = kama.iloc[i - 1] + sc.iloc[i] * (data.iloc[i] - kama.iloc[i - 1])
        return kama

    elif method == "tma":
        sma1 = cast(Series, data.rolling(window=window).mean())
        sma2 = cast(Series, sma1.rolling(window=window).mean())
        return sma2

    raise ValueError(f"Invalid method: {method}")

"""Module to process stock data by applying moving averages."""

from typing import Literal, cast

import pandas as pd

from app.logger import setup_logger
from app.moving_avg import calculate_moving_average
from app.output_handler import send_to_output

# Initialize logger
logger = setup_logger(__name__)

# Supported moving average methods
VALID_METHODS = {"sma", "ema", "wma", "hma", "vwap", "dema", "tema", "kama", "tma"}

MovingAvgMethod = Literal["sma", "ema", "wma", "hma", "vwap", "dema", "tema", "kama", "tma"]


def process_stock_data(
    stock_data: pd.DataFrame, window_size: int, ma_method: MovingAvgMethod = "sma"
) -> pd.DataFrame:
    """Apply the specified moving average method to stock data and output the result.

    Args:
      stock_data(pd.DataFrame): DataFrame containing 'Close' and optionally 'Volume'.
      window_size(int): Window size for the moving average.
      ma_method(MovingAvgMethod): Type of moving average.
      stock_data: pd.DataFrame:
      window_size: int:
      ma_method: MovingAvgMethod:  (Default value = "sma")
      stock_data: pd.DataFrame:
      window_size: int:
      ma_method: MovingAvgMethod:  (Default value = "sma")

    Returns:
      pd.DataFrame: DataFrame with an additional column for the moving average.

    """
    try:
        if stock_data.empty:
            logger.warning("Input stock data is empty.")
            return pd.DataFrame()

        if ma_method not in VALID_METHODS:
            logger.error(f"Invalid moving average method: {ma_method}")
            return pd.DataFrame()

        if "Close" not in stock_data.columns:
            logger.error("Missing 'Close' column in stock data.")
            return pd.DataFrame()

        if not pd.api.types.is_numeric_dtype(stock_data["Close"]):
            logger.error("'Close' column must be numeric.")
            return pd.DataFrame()

        if ma_method == "vwap" and "Volume" not in stock_data.columns:
            logger.error("VWAP method requires a 'Volume' column.")
            return pd.DataFrame()

        if window_size > len(stock_data):
            logger.warning("Window size is larger than dataset length. Adjusting window.")
            window_size = len(stock_data)

        column_name = f"{ma_method.upper()}_{window_size}"
        close_series = cast(pd.Series, stock_data["Close"])
        volume_series = cast(pd.Series, stock_data["Volume"]) if ma_method == "vwap" else None

        ma_series = calculate_moving_average(
            data=close_series,
            window=window_size,
            method=ma_method,
            volume=volume_series,
        )
        stock_data[column_name] = ma_series

        symbol = stock_data["symbol"].iloc[0] if "symbol" in stock_data.columns else "N/A"
        logger.info(f"Calculated {column_name} for symbol: {symbol}")

        send_to_output(
            {
                "symbol": symbol,
                "analysis_type": "movavg",
                "method": ma_method,
                "window": window_size,
                "result": stock_data.tail(1).to_dict(orient="records")[0],
            }
        )

        return stock_data

    except Exception:
        logger.exception("Unhandled error while processing stock data")
        return pd.DataFrame()

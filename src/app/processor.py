"""Module to process stock data by applying moving averages."""

import pandas as pd

from app.logger import setup_logger
from app.moving_avg import calculate_moving_average

# Initialize logger
logger = setup_logger(__name__)

# Supported moving average methods
VALID_METHODS = {"sma", "ema", "wma", "hma"}


def process_stock_data(
    stock_data: pd.DataFrame, window_size: int, ma_method: str = "sma"
) -> pd.DataFrame:
    """Apply the specified moving average method to stock data.

    This function processes stock data by calculating a moving average
    using a specified method and window size. It adds the resulting moving
    average as a new column in the DataFrame.

    Args:
    ----
        stock_data (pd.DataFrame): DataFrame containing stock 'Close' prices.
        window_size (int): Window size for the moving average.
        ma_method (str, optional): Type of moving average ('sma', 'ema', 'wma', 'hma').
                                   Defaults to "sma".

    Returns:
    -------
        pd.DataFrame: DataFrame with an additional column for the moving average.
                      If an error occurs, returns an empty DataFrame.

    """
    try:
        # Validate moving average method
        if ma_method.lower() not in VALID_METHODS:
            logger.error(f"Invalid moving average method: {ma_method}")
            return pd.DataFrame()

        # Ensure 'Close' column exists
        if "Close" not in stock_data.columns:
            logger.error("Missing 'Close' column in stock data.")
            return pd.DataFrame()

        # Build column name and calculate MA
        column_name = f"{ma_method.upper()}_{window_size}"
        stock_data[column_name] = calculate_moving_average(
            stock_data["Close"], window_size, ma_method
        )

        # Log symbol (if column exists)
        symbol = stock_data["symbol"].iloc[0] if "symbol" in stock_data else "N/A"
        logger.info(f"Calculated {column_name} for symbol: {symbol}")
        return stock_data

    except Exception:
        logger.exception("Unhandled error while processing stock data")
        return pd.DataFrame()

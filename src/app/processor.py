"""
Module to process stock data by applying moving averages.
"""

import pandas as pd
from src.app.moving_avg import calculate_moving_average
from src.app.logger import setup_logger

logger = setup_logger()

def process_stock_data(
    stock_data: pd.DataFrame, window_size: int, ma_method: str = "sma"
) -> pd.DataFrame:
    """
    Apply the specified moving average method to stock data.

    Args:
        stock_data (pd.DataFrame): DataFrame containing stock 'Close' prices.
        window_size (int): Window size for the moving average.
        ma_method (str, optional): Type of moving average ('sma', 'ema', 'wma', 'hma'). Defaults to "sma".

    Returns:
        pd.DataFrame: DataFrame with an additional column for the moving average.
    """
    try:
        column_name = f"{ma_method.upper()}_{window_size}"
        stock_data[column_name] = calculate_moving_average(
            stock_data["Close"], window_size, ma_method
        )
        logger.info(f"Calculated {column_name}.")
        return stock_data
    except Exception as error:
        logger.error(f"Error in processing stock data: {error}")
        return pd.DataFrame()


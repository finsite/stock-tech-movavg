# """
# Processes stock data by applying moving averages.
# """

# import pandas as pd
# from moving_avg import calculate_moving_average
# from logger import setup_logger

# logger = setup_logger()


# def process_stock_data(
#     data: pd.DataFrame, window: int, method: str = "sma"
# ) -> pd.DataFrame:
#     """
#     Applies the chosen moving average method to stock data.

#     :param data: DataFrame containing stock 'Close' prices
#     :param window: Window size for the moving average
#     :param method: Type of moving average ('sma', 'ema', 'wma', 'hma')
#     :return: DataFrame with moving average column added
#     """
#     try:
#         data[f"{method.upper()}_{window}"] = calculate_moving_average(
#             data["Close"], window, method
#         )
#         logger.info(f"Successfully calculated {method.upper()} for window {window}.")
#         return data
#     except Exception as e:
#         logger.error(f"Error processing stock data: {e}")
#         return None
"""
Processes stock data by applying moving averages.
"""

import pandas as pd
from src.app.moving_avg import calculate_moving_average  # ✅ Fixed import
from src.app.logger import setup_logger  # ✅ Fixed import

logger = setup_logger()


def process_stock_data(
    data: pd.DataFrame, window: int, method: str = "sma"
) -> pd.DataFrame:
    """
    Applies the chosen moving average method to stock data.

    Args:
        data (pd.DataFrame): DataFrame containing stock 'Close' prices.
        window (int): Window size for the moving average.
        method (str, optional): Type of moving average ('sma', 'ema', 'wma', 'hma'). Defaults to "sma".

    Returns:
        pd.DataFrame: DataFrame with moving average column added.
    """
    try:
        data[f"{method.upper()}_{window}"] = calculate_moving_average(
            data["Close"], window, method
        )
        logger.info(f"Successfully calculated {method.upper()} for window {window}.")
        return data
    except Exception as e:
        logger.error(f"Error processing stock data: {e}")
        return pd.DataFrame()  # ✅ Return an empty DataFrame instead of None

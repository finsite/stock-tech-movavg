"""
Entry point for Stock-Tech-MovAvg.
Loads stock data, calculates moving averages, and publishes results.
"""

import pandas as pd
from processor import process_stock_data
from queue_sender import publish_to_queue


def main():
    """
    Main function that loads stock data, applies moving averages, and publishes results.
    """
    stock_data = pd.DataFrame(
        {
            "Date": pd.date_range(start="2024-01-01", periods=10, freq="D"),
            "Close": [100, 102, 101, 103, 105, 107, 106, 108, 110, 112],
        }
    )

    ma_type = "sma"
    window = 3

    processed_data = process_stock_data(stock_data, window, ma_type)

    if processed_data is not None:
        publish_to_queue(processed_data.to_dict(orient="records"))


if __name__ == "__main__":
    main()

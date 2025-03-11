"""
Unit tests for stock data processing.
"""

import os
import sys
import pandas as pd

# Ensure `src` is in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from src.app.processor import process_stock_data  # ✅ Fixed import


def test_process_stock_data():
    """
    Test the stock data processing function.
    """
    data = pd.DataFrame({"Close": [1, 2, 3, 4, 5]})
    window = 3
    method = "sma"
    result = process_stock_data(data, window=window, method=method)

    assert result is not None, "Processing failed"
    assert isinstance(result, pd.DataFrame), "Processed result is not a DataFrame"

    # Generate expected column name dynamically
    expected_column = f"{method.upper()}_{window}"

    assert (
        expected_column in result.columns
    ), f"Processed result missing '{expected_column}' column"

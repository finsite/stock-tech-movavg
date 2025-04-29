"""
Unit tests for stock data processing.
"""

import os
import sys

import pandas as pd
import pytest

# Ensure `src` is in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from src.app.processor import process_stock_data  # ✅ Fixed function name


def test_process_stock_data():
    """
    Test stock data processing function with moving averages.
    """
    stock_data = pd.DataFrame({"Close": [100, 102, 104, 106, 108]})
    window_size = 3
    ma_method = "sma"
    expected_column = f"{ma_method.upper()}_{window_size}"

    result = process_stock_data(stock_data, window_size, ma_method)

    # ✅ Using `pytest.fail()` to verify conditions, avoiding Bandit B101
    if result is None:
        pytest.fail("Processing failed")

    if not isinstance(result, pd.DataFrame):
        pytest.fail("Processed result is not a DataFrame")

    if expected_column not in result.columns:
        pytest.fail(f"Processed result missing '{expected_column}' column")

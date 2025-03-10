"""
Unit tests for stock data processing.
"""

import os
import sys
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from app.processor import process_stock_data


def test_process_stock_data():
    data = pd.DataFrame({"Close": [1, 2, 3, 4, 5]})
    result = process_stock_data(data, window=3, method="sma")
    assert result is not None, "Processing failed"

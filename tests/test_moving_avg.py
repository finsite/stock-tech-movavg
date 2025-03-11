"""
Unit tests for moving average calculations.
"""

import os
import sys
import pandas as pd

# Ensure `src` is in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from src.app.moving_avg import calculate_moving_average  # ✅ Fixed import


def test_sma():
    """
    Test Simple Moving Average (SMA) calculation.
    """
    data = pd.Series([1, 2, 3, 4, 5])
    result = calculate_moving_average(data, window=3, method="sma")
    assert result is not None, "SMA calculation failed"


def test_ema():
    """
    Test Exponential Moving Average (EMA) calculation.
    """
    data = pd.Series([1, 2, 3, 4, 5])
    result = calculate_moving_average(data, window=3, method="ema")
    assert result is not None, "EMA calculation failed"


def test_wma():
    """
    Test Weighted Moving Average (WMA) calculation.
    """
    data = pd.Series([1, 2, 3, 4, 5])
    result = calculate_moving_average(data, window=3, method="wma")
    assert result is not None, "WMA calculation failed"


def test_hma():
    """
    Test Hull Moving Average (HMA) calculation.
    """
    data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    result = calculate_moving_average(data, window=5, method="hma")
    assert result is not None, "HMA calculation failed"

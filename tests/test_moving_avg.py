"""
Unit tests for moving average calculations.
"""
import os
import sys
import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from app.moving_avg import calculate_moving_average

def test_sma():
    data = pd.Series([1, 2, 3, 4, 5])
    result = calculate_moving_average(data, window=3, method="sma")
    assert result is not None, "SMA calculation failed"

def test_ema():
    data = pd.Series([1, 2, 3, 4, 5])
    result = calculate_moving_average(data, window=3, method="ema")
    assert result is not None, "EMA calculation failed"

def test_wma():
    data = pd.Series([1, 2, 3, 4, 5])
    result = calculate_moving_average(data, window=3, method="wma")
    assert result is not None, "WMA calculation failed"

def test_hma():
    data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    result = calculate_moving_average(data, window=5, method="hma")
    assert result is not None, "HMA calculation failed"
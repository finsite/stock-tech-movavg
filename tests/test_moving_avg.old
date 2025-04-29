"""
Unit tests for moving average calculations.
"""

import os
import sys

import pandas as pd
import pytest

# Ensure `src` is in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from src.app.moving_avg import (  # ✅ Import the actual function being tested
    calculate_moving_average,
)


@pytest.mark.parametrize("method", ["sma", "ema", "wma", "hma"])
def test_moving_average(method):
    """
    Parametrized test for different moving average methods.
    """
    data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    result = calculate_moving_average(data, window=3, method=method)

    # ✅ Replaced assert with pytest exceptions to fix Bandit B101
    if result is None:
        pytest.fail(f"{method.upper()} calculation failed")

    if not isinstance(result, pd.Series):
        pytest.fail(f"{method.upper()} should return a pandas Series")

    if len(result) != len(data):
        pytest.fail(f"{method.upper()} output length mismatch")

"""
Unit tests for queue handling.
"""

import os
import sys
import pytest

# Ensure `src` is in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from src.app.queue_sender import send_to_rabbitmq, send_to_sqs  # ✅ Fixed import


def test_send_to_rabbitmq():
    """
    Test RabbitMQ message sending.
    """
    try:
        send_to_rabbitmq({"test": "data"})
    except Exception as e:
        pytest.fail(f"RabbitMQ sending failed: {e}")


def test_send_to_sqs():
    """
    Test SQS message sending.
    """
    try:
        send_to_sqs({"test": "data"})
    except Exception as e:
        pytest.fail(f"SQS sending failed: {e}")

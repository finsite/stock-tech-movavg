"""
Unit tests for queue handling.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from app.queue_handler import send_to_rabbitmq, send_to_sqs


def test_send_to_rabbitmq():
    try:
        send_to_rabbitmq({"test": "data"})
    except Exception:
        assert False, "RabbitMQ sending failed"


def test_send_to_sqs():
    try:
        send_to_sqs({"test": "data"})
    except Exception:
        assert False, "SQS sending failed"

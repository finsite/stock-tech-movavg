"""Handles message queue interactions for RabbitMQ and SQS.

This module provides functions to send data to RabbitMQ and SQS message queues.
"""

import json
import os

import boto3
import pika

from src.app.logger import setup_logger

logger = setup_logger()

SQS_CLIENT = boto3.client("sqs", region_name=os.getenv("AWS_REGION", "us-east-1"))


def send_to_rabbitmq(data: dict) -> None:
    """Sends data to RabbitMQ.

    :param data: Dictionary containing data to be sent to RabbitMQ
    """
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST", "rabbitmq"))
        )
        channel = connection.channel()
        channel.basic_publish(
            exchange=os.getenv("RABBITMQ_EXCHANGE", "stock_exchange"),
            routing_key=os.getenv("RABBITMQ_ROUTING_KEY", "moving_avg"),
            body=json.dumps(data),
        )
        connection.close()
    except Exception as e:
        logger.error(f"Failed to send data to RabbitMQ: {e}")


def send_to_sqs(data: dict) -> None:
    """Sends data to AWS SQS.

    :param data: Dictionary containing data to be sent to SQS
    """
    try:
        response = SQS_CLIENT.send_message(
            QueueUrl=os.getenv("AWS_SQS_QUEUE_URL", ""), MessageBody=json.dumps(data)
        )
        logger.info(f"Published data to SQS, MessageId: {response['MessageId']}")
    except Exception as e:
        logger.error(f"Failed to send data to SQS: {e}")

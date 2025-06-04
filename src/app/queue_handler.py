"""Handles message queue consumption for RabbitMQ and SQS.

This module receives stock data, applies moving average analysis, and
sends processed results to the output handler.
"""

import json
import os
import time
from typing import cast

import boto3
import pika
from botocore.exceptions import BotoCoreError, NoCredentialsError

from app.logger import setup_logger
from app.output_handler import send_to_output
from app.processor import MovingAvgMethod, process_stock_data

logger = setup_logger(__name__)

# Environment variables for dynamic config
QUEUE_TYPE = os.getenv("QUEUE_TYPE", "rabbitmq").lower()
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", "stock_analysis")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "analysis_queue")
RABBITMQ_ROUTING_KEY = os.getenv("RABBITMQ_ROUTING_KEY", "#")

SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL", "")
SQS_REGION = os.getenv("SQS_REGION", "us-east-1")

# Moving average config
MA_TYPE = os.getenv("MOVING_AVERAGE_TYPE", "sma")
WINDOW_SIZE = int(os.getenv("MOVING_AVERAGE_WINDOW", "5"))

# Init boto3 client
sqs_client = None
if QUEUE_TYPE == "sqs":
    try:
        sqs_client = boto3.client("sqs", region_name=SQS_REGION)
        logger.info(f"SQS client initialized for region {SQS_REGION}")
    except (BotoCoreError, NoCredentialsError) as e:
        logger.error("Failed to initialize SQS client: %s", e)
        sqs_client = None


def connect_to_rabbitmq() -> pika.BlockingConnection:
    """Establishes and returns a RabbitMQ connection with retries."""
    retries = 5
    while retries > 0:
        try:
            conn = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            if conn.is_open:
                logger.info("Connected to RabbitMQ")
                return conn
        except Exception as e:
            retries -= 1
            logger.warning("RabbitMQ connection failed: %s. Retrying in 5s...", e)
            time.sleep(5)
    raise ConnectionError("Could not connect to RabbitMQ after retries")


def consume_rabbitmq() -> None:
    """Consumes messages from RabbitMQ and processes them with moving average
    analysis.


    """
    connection = connect_to_rabbitmq()
    channel = connection.channel()

    channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type="topic", durable=True)
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    channel.queue_bind(
        exchange=RABBITMQ_EXCHANGE, queue=RABBITMQ_QUEUE, routing_key=RABBITMQ_ROUTING_KEY
    )

    def callback(ch, method, properties, body: bytes) -> None:
        """Args:
        ----
          ch:
          method:
          properties:
          body: bytes:
          body: bytes:
          body: bytes:

        :param ch: param method:
        :param properties: param body: bytes:
        :param method: param body: bytes:
        :param body: bytes:
        :param body: type body: bytes :
        :param body: type body: bytes :
        :param body: bytes:
        :param body: bytes:
        :param body: bytes:
        :param body: bytes: 

        """
        try:
            message = json.loads(body)
            logger.info("Received message: %s", message)

            df = process_stock_data(
                stock_data=message["data"],
                window_size=WINDOW_SIZE,
                ma_method=cast(MovingAvgMethod, MA_TYPE),
            )
            result = {
                "symbol": message.get("symbol"),
                "timestamp": message.get("timestamp"),
                "source": "MovingAverage",
                "analysis": df.to_dict(orient="records"),
            }

            send_to_output(result)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except json.JSONDecodeError:
            logger.error("Invalid JSON: %s", body)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as e:
            logger.error("Error processing message: %s", e)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback)
    logger.info("Waiting for messages from RabbitMQ...")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        logger.info("Gracefully stopping RabbitMQ consumer...")
        channel.stop_consuming()
    finally:
        connection.close()
        logger.info("RabbitMQ connection closed.")


def consume_sqs() -> None:
    """Consumes messages from AWS SQS and processes them with moving average
    analysis.


    """
    if not sqs_client or not SQS_QUEUE_URL:
        logger.error("SQS not initialized or missing queue URL.")
        return

    logger.info("Polling for SQS messages...")

    while True:
        try:
            response = sqs_client.receive_message(
                QueueUrl=SQS_QUEUE_URL,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=10,
            )

            for msg in response.get("Messages", []):
                try:
                    body = json.loads(msg["Body"])
                    logger.info("Received SQS message: %s", body)

                    df = process_stock_data(
                        stock_data=body["data"],
                        window_size=WINDOW_SIZE,
                        ma_method=cast(MovingAvgMethod, MA_TYPE),
                    )
                    result = {
                        "symbol": body.get("symbol"),
                        "timestamp": body.get("timestamp"),
                        "source": "MovingAverage",
                        "analysis": df.to_dict(orient="records"),
                    }

                    send_to_output(result)
                    sqs_client.delete_message(
                        QueueUrl=SQS_QUEUE_URL, ReceiptHandle=msg["ReceiptHandle"]
                    )
                    logger.info("Deleted SQS message: %s", msg["MessageId"])
                except Exception as e:
                    logger.error("Error processing SQS message: %s", e)
        except Exception as e:
            logger.error("SQS polling failed: %s", e)
            time.sleep(5)


def consume_messages() -> None:
    """Selects the consumer based on QUEUE_TYPE environment variable."""
    if QUEUE_TYPE == "rabbitmq":
        consume_rabbitmq()
    elif QUEUE_TYPE == "sqs":
        consume_sqs()
    else:
        logger.error("Invalid QUEUE_TYPE specified. Use 'rabbitmq' or 'sqs'.")

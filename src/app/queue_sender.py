"""
Handles message queue interactions for RabbitMQ and SQS.
"""
import os
import pika
import boto3
import json
from logger import setup_logger

logger = setup_logger()

sqs_client = boto3.client("sqs", region_name=os.getenv("AWS_REGION", "us-east-1"))

def send_to_rabbitmq(data: dict):
    """
    Sends data to RabbitMQ.
    """
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST", "rabbitmq")))
        channel = connection.channel()
        channel.basic_publish(exchange=os.getenv("RABBITMQ_EXCHANGE", "stock_exchange"),
                              routing_key=os.getenv("RABBITMQ_ROUTING_KEY", "moving_avg"),
                              body=json.dumps(data))
        logger.info("Published data to RabbitMQ")
        connection.close()
    except Exception as e:
        logger.error(f"Failed to send data to RabbitMQ: {e}")

def send_to_sqs(data: dict):
    """
    Sends data to AWS SQS.
    """
    try:
        response = sqs_client.send_message(QueueUrl=os.getenv("AWS_SQS_QUEUE_URL", ""), MessageBody=json.dumps(data))
        logger.info(f"Published data to SQS, MessageId: {response['MessageId']}")
    except Exception as e:
        logger.error(f"Failed to send data to SQS: {e}")
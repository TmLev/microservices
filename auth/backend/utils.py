# coding=utf-8

import os
import json

import pika


class MessageQueueProvider:
    """
    Provides messages to RabbitMQ.
    """

    def __init__(
        self,
    ):
        self.connection_ = None
        return

    def send_confirmation(
        self,
        receipt: str,
        token: str,
        queue: str = "auth-email-confirmation",
    ):
        if not self.connection_:
            self.connection_ = pika.BlockingConnection(  # TODO: close connection(
                parameters=pika.ConnectionParameters(
                    host="mq",
                    port=os.environ.get("MQ_PORT")
                )
            )

        channel = self.connection_.channel()
        channel.queue_declare(
            queue=queue
        )

        body = json.dumps(
            obj={
                "receipt": receipt,
                "url":     token,  # TODO: make url
            }
        )

        channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=body,
        )

        return


message_queue_provider = MessageQueueProvider()

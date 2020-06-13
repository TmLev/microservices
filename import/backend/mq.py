# coding=utf-8

import os
import pika
import json


class MessageQueueConsumer:
    """
    Provides messages to RabbitMQ.
    """

    def __init__(
        self,
    ) -> None:
        self.connection = None
        self.channel = None
        return

    def _restore_connection(self):
        self.connection = pika.BlockingConnection(
            parameters=pika.ConnectionParameters(
                host=os.environ.get("MQ_HOST"),
                port=int(os.environ.get("MQ_PORT")),
                heartbeat=None,
            )
        )
        self.channel = self.connection.channel()

    def get_path_to_ready_chunk(
        self,
        queue: str = os.environ.get("IMPORT_QUEUE")
    ) -> str:
        if not self.connection or self.connection.is_closed:
            self._restore_connection()

        method_frame, header_frame, body = self.channel.basic_get(queue)
        if not method_frame:
            return ""

        self.channel.basic_ack(method_frame.delivery_tag)

        path = json.loads(body)["path"]
        print(f"received from broker: {path = }")

        return path

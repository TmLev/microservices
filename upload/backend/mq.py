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
    ) -> None:
        self.connection_ = None
        return

    def _restore_connection(self):
        self.connection_ = pika.BlockingConnection(
            parameters=pika.ConnectionParameters(
                host=os.environ.get("MQ_HOST"),
                port=int(os.environ.get("MQ_PORT")),
                heartbeat=None,
            )
        )

    def chunk_ready(
        self,
        path: str,
        queue: str = os.environ.get("IMPORT_QUEUE")
    ) -> None:
        if not self.connection_ or self.connection_.is_closed:
            self._restore_connection()

        channel = self.connection_.channel()
        channel.queue_declare(queue)

        body = json.dumps(
            obj={
                "path": path,
            }
        )

        channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=body,
        )

        return

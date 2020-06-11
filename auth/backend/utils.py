# coding=utf-8

import os
import json
import socket

import typing as tp

import pika

from django.urls import reverse


class MessageQueueProvider:
    """
    Provides messages to RabbitMQ.
    """

    def __init__(
        self,
    ) -> None:
        self.connection_ = None
        return

    def send_confirmation(
        self,
        queue: str,
        recipient: str,
        subject: str,
        body: str,
        retry_count: int = 5,
    ) -> None:
        if not self.connection_ or self.connection_.is_closed:
            self.connection_ = pika.BlockingConnection(
                parameters=pika.ConnectionParameters(
                    host=os.environ.get("MQ_HOST"),
                    port=int(os.environ.get("MQ_PORT")),
                    heartbeat=None,
                )
            )

        channel = self.connection_.channel()
        channel.queue_declare(
            queue=queue
        )

        body = json.dumps(
            obj={
                "recipient":   recipient,
                "subject":     subject,
                "body":        body,
                "retry_count": retry_count,
            }
        )

        channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=body,
        )

        return


message_queue_provider = MessageQueueProvider()


def make_confirmation_message(
    view,
    confirmation_token,
) -> str:
    """
    Assemble link to according view.
    """

    greeting = "<p>Hello!</p>\n"
    prefix = "<p>Please, click confirmation link below to complete your registration:</p>\n"

    host_and_port = get_local_network_ip() + ":" + os.environ.get("AUTH_PORT")
    confirm_registration_url = host_and_port + reverse(view, **{}) + f"?token={str(confirmation_token)}"
    link = str(confirm_registration_url)

    print(confirm_registration_url)

    return "".join([greeting, prefix, link])


def get_according_notification_queue(
    prefix: str,
) -> str:
    """
    Parse NOTIFICATION_QUEUES environment variable.
    :param prefix: queue name prefix.
    :return: queue name
    """

    notification_queues: tp.List[str] = os.environ.get("NOTIFICATION_QUEUES").split(",")

    for queue in notification_queues:
        if queue.startswith(prefix):
            return queue

    return "default"


def get_local_network_ip():
    return "http://192.168.1.71"

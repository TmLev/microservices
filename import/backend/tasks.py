# coding=utf-8

import json
import time
import os
import typing as tp

from django_q.tasks import async_task

from backend.models import Product
from backend.mq import MessageQueueConsumer


DELAY = 0  # seconds


def insert_chunk(products: tp.List[tp.Dict[str, str]]) -> None:
    for product in products:
        product_db, created = Product.objects.get_or_create(
            id=product["id"],
            title=product["title"],
            category=product["category"],
        )
        if created:
            product_db.save()

    async_task(schedule_import_chunk)


def parse_chunk(path: str) -> None:
    chunk = []

    if os.path.exists(path):
        with open(path) as file:
            chunk = json.load(file)

    async_task(insert_chunk, chunk)


def import_chunk():
    global DELAY

    mq_consumer = MessageQueueConsumer()

    path = mq_consumer.get_path_to_ready_chunk()
    if path:
        DELAY = 0
    else:
        DELAY = 2

    async_task(parse_chunk, path)


def schedule_import_chunk():
    async_task(import_chunk)
    time.sleep(DELAY)


async_task(schedule_import_chunk)

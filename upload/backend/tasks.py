# coding=utf-8

import json
import typing as tp

from django_q.tasks import async_task

from backend.mq import MessageQueueProvider
from backend.readers import (
    CSVReader,
    XMLReader,
)


def notify_import(task) -> None:
    path = task.result
    mq_provider = MessageQueueProvider()
    mq_provider.chunk_ready(path)


def save_to_file(chunk: tp.List[tp.Dict[str, str]], path: str) -> str:
    with open(path, "w") as file:
        json.dump(chunk, file)

    return path


def _async_import(path: str, format_: str):
    reader = CSVReader(path) if format_ == "csv" else XMLReader(path)

    index = 0
    while chunk := reader.read_chunk():
        chunk_path = path + f"_chunk_{index}"
        async_task(save_to_file, chunk, chunk_path, hook=notify_import)
        index += 1


def async_import(path: str, format_: str) -> None:
    async_task(_async_import, path, format_)

# coding=utf-8

import csv
import xml.etree.ElementTree as ET
from abc import (
    ABC,
    abstractmethod,
)


CHUNK_SIZE = 512


class BaseReader(ABC):

    @abstractmethod
    def read_chunk(self):
        pass


class CSVReader(BaseReader):

    def __init__(self, path: str) -> None:
        self.file = open(path)
        self.reader = csv.reader(self.file)
        self.headers = next(self.reader)

    def read_chunk(self):
        chunk = []

        for _, row in zip(range(CHUNK_SIZE), self.reader):
            chunk.append({
                header: value
                for header, value in zip(self.headers, row)
            })

        return chunk


class XMLReader(BaseReader):

    def __init__(self, path: str) -> None:
        self.root = ET.parse(path).getroot()
        self.products = self.root.iterfind("product")

    def read_chunk(self):
        chunk = []

        for _, product in zip(range(CHUNK_SIZE), self.products):
            chunk.append({
                elem.tag: elem.text
                for elem in product
            })

        return chunk

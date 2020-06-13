# coding=utf-8

import os
import hashlib

import typing as tp

from django.core.files import File


def compute_blake2b_hash(
    file
) -> str:
    """
    Compute blake2b hash for given file (must be open).
    :param file: file-like object with `.read` method.
    :return: computed hash.
    """

    file_hash = hashlib.blake2b()

    while chunk := file.read(8192):
        file_hash.update(chunk)

    return file_hash.hexdigest()


def save_to_tempdir(file: File) -> tp.Tuple[str, bool]:
    """
    Save open file to disk using blake2b hash.
    :param file: open Django file.
    :return: whether file already exists.
    """

    file_hash = compute_blake2b_hash(file)
    path = os.path.join("/tmp/files", file_hash)

    if os.path.exists(path):
        return "", True

    with open(path, "wb") as tempfile:
        for chunk in file.chunks():
            tempfile.write(chunk)

    return path, False

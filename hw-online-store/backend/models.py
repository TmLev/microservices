# coding=utf-8

from __future__ import annotations

import uuid

from django.db import models


class Product(models.Model):
    title = models.TextField(
    )
    category = models.TextField(
    )
    code = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    @staticmethod
    def get_by_code(
        code: uuid.UUID,
    ) -> Product:
        return Product.objects.get(code=code)

    @staticmethod
    def create(
        title: str,
        category: str,
    ) -> uuid.UUID:
        product: Product = Product(
            title=title,
            category=category,
        )
        product.save()
        return product.code

    @staticmethod
    def delete_by_code(
        code: uuid.UUID,
    ) -> None:
        product: Product = Product.get_by_code(code)
        product.delete()


    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


    def __str__(
        self
    ) -> str:
        return self.title

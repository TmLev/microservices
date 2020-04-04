# coding=utf-8

import uuid

from django.db import models


class Product(models.Model):
    title = models.TextField(
    )
    category = models.TextField(
    )

    @staticmethod
    def get_by_id(
        id_: int,
    ) -> 'Product':
        return Product.objects.get(id=id_)

    @staticmethod
    def create(
        title: str,
        category: str,
    ) -> int:
        product: Product = Product(
            title=title,
            category=category,
        )
        product.save()
        return product.id

    @staticmethod
    def delete_by_id(
        id_: int,
    ) -> None:
        product: Product = Product.get_by_id(id_)
        product.delete()
        return


    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


    def __str__(
        self
    ) -> str:
        return self.title

# coding=utf-8

import hashlib

from django.db import models


class Product(models.Model):
    id = models.TextField(
        primary_key=True,
    )
    title = models.TextField(
    )
    category = models.TextField(
    )

    @staticmethod
    def get_by_id(
        id_: str,
    ) -> 'Product':
        return Product.objects.get(id=id_)

    @staticmethod
    def create(
        title: str,
        category: str,
        id_: str = "",
    ) -> str:
        hash_ = id_ or hashlib.blake2s(
            data=(title + category).encode(),
        ).hexdigest()

        product: Product = Product(
            id=hash_,
            title=title,
            category=category,
        )

        product.save()

        return product.id

    @staticmethod
    def delete_by_id(
        id_: str,
    ) -> None:
        if id_ == "all":
            Product.objects.all().delete()
            return

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

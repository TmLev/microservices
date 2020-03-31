# coding=utf-8

from django.contrib import admin

from backend.models import Product


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = [
        "id",
    ]


admin.site.register(Product, ProductAdmin)

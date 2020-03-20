# coding=utf-8

from rest_framework import serializers

from backend.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["title", "category", "code"]

# coding=utf-8

import requests
import os

from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)

from backend.models import Product
from backend.serializers import ProductSerializer


def is_token_valid(
    request: Request,
) -> bool:
    """
    Validate authorization token using another service.
    :param request: request with header with token.
    :return: is token valid or not.
    """

    token = request.META.get("HTTP_AUTHORIZATION", "").split("Bearer ")[-1]

    token_response: requests.Response = requests.post(
        url="http://auth:" + os.environ.get("AUTH_PORT") + "/api/verify_token",
        data={
            "token": token,
        },
    )

    return token_response.status_code == HTTP_200_OK


class ProductView(APIView):
    """
    ProductView provides handlers for different methods on single product.
    """

    def get(
        self,
        request: Request,
    ) -> Response:
        """
        Get info about product by its id.
        :param request: request with "id" field.
        :return: response whether request is successful with info about product.
        """

        id_from_query: str = request.query_params.get("id")
        try:
            id_: int = int(id_from_query)
            product: Product = Product.get_by_id(id_)
        except (ValueError, TypeError, Product.DoesNotExist):
            return Response(
                data={
                    "message": "No product with such id.",
                },
                status=HTTP_404_NOT_FOUND,
            )

        serializer = ProductSerializer(
            product,
            many=False,
        )

        return Response(
            data=serializer.data,
            status=HTTP_200_OK,
        )

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Edit product info.
        :param request: request with "id" and optional "title" and "category" fields.
        :return: response whether request is successful.
        """

        if not is_token_valid(request):
            return Response(
                data={
                    "message": "Invalid credentials."
                },
                status=HTTP_401_UNAUTHORIZED,
            )

        id_from_query: str = request.data.get("id")
        try:
            id_: int = int(id_from_query)
            product: Product = Product.get_by_id(id_)
        except (ValueError, TypeError, Product.DoesNotExist):
            return Response(
                data={
                    "message": "No product with such id."
                },
                status=HTTP_404_NOT_FOUND,
            )

        title: str = request.data.get("title")
        if title:
            product.title = title

        category: str = request.data.get("category")
        if category is not None:
            product.category = category

        product.save()

        return Response(
            data={
                "message": "Product info was edited successfully.",
            },
            status=HTTP_200_OK,
        )

    def put(
        self,
        request: Request,
    ) -> Response:
        """
        Create new product.
        :param request: request with "title" and optional "category" string fields.
        :return: response whether request is successful.
        """

        if not is_token_valid(request):
            return Response(
                data={
                    "message": "Invalid credentials."
                },
                status=HTTP_401_UNAUTHORIZED,
            )

        title: str = request.data.get("title")
        if not title:
            return Response(
                data={
                    "message": "Title must not be empty.",
                },
                status=HTTP_400_BAD_REQUEST,
            )

        category: str = request.data.get("category")

        id_ = Product.create(
            title=title,
            category=category,
        )

        return Response(
            data={
                "id": id_,
            },
            status=HTTP_200_OK,
        )

    def delete(
        self,
        request: Request,
    ) -> Response:
        """
        Delete product by its id.
        :param request: request with "id" field (must be string).
        :return: response whether request is successful.
        """

        if not is_token_valid(request):
            return Response(
                data={
                    "message": "Invalid credentials."
                },
                status=HTTP_401_UNAUTHORIZED,
            )

        id_from_query: str = request.data.get("id")
        try:
            id_: int = int(id_from_query)
            Product.delete_by_id(id_)
        except (TypeError, ValueError, Product.DoesNotExist):
            return Response(
                data={
                    "message": "No product with such id.",
                },
                status=HTTP_404_NOT_FOUND,
            )

        return Response(
            data={
                "message": "Product was deleted successfully.",
            },
            status=HTTP_200_OK,
        )


class ListProductView(ListAPIView):
    """
    List view for multiple products.
    """


    class Pagination(PageNumberPagination):
        page_size_query_param = "page_size"
        page_size = 4


    queryset = Product.objects.all().order_by("title")
    serializer_class = ProductSerializer
    pagination_class = Pagination


@api_view(["PUT"])
def populate(
    request: Request,
) -> Response:
    """
    Populate database with fake products.
    :param request: empty request
    :return: response whether request is successful
    """

    for title, category in [
        ("fork", "cutlery"),
        ("lexus", "cars"),
        ("house", "realty"),
        ("notebook", "books"),
        ("bible", "books"),
        ("mug", "cutlery"),
        ("phone", "electronics"),
        ("door", "furniture"),
        ("chair", "furniture")
    ]:
        product, _ = Product.objects.get_or_create(
            title=title,
            category=category,
        )
        product.save()

    return Response(
        data={
            "message": "Database populated successfully.",
        },
        status=HTTP_200_OK,
    )

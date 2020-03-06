# coding=utf-8

import uuid

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from backend.models import Product


class ProductView(APIView):
    """
    ProductView provides handlers for different methods on single product
    """

    parser_classes = [
        JSONParser,
    ]

    def get(
        self,
        request: Request,
    ) -> Response:
        """
        Get info about product by its code.
        :param request: request with "code" field
        :return: response whether request is successful
        """

        code_from_query: str = request.query_params.get("code", "")
        try:
            code: uuid.UUID = uuid.UUID(code_from_query)
            product: Product = Product.get_by_code(code)
        except (ValueError, TypeError, Product.DoesNotExist):
            return Response(
                data="No product with such code.",
                status=HTTP_404_NOT_FOUND,
            )

        return Response(
            data=product.to_dict(),
            status=HTTP_200_OK,
        )

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Edit product info.
        :param request: request with "code" and optional "title" and "category" fields
        :return: response whether request is successful
        """

        code_from_query: str = request.query_params.get("code", "")
        print(code_from_query)
        try:
            code: uuid.UUID = uuid.UUID(code_from_query)
            product: Product = Product.get_by_code(code)
        except (ValueError, TypeError, Product.DoesNotExist):
            return Response(
                data="No product with such code.",
                status=HTTP_404_NOT_FOUND,
            )

        title: str = request.query_params.get("title")
        if title:
            print("TITLE", title)
            product.title = title

        category: str = request.query_params.get("category")
        if category is not None:
            product.category = category

        product.save()

        return Response(
            data="Product info was edited succesfully.",
            status=HTTP_200_OK,
        )

    def put(
        self,
        request: Request,
    ) -> Response:
        """
        Create new product.
        :param request: request with "title" and optional "category" fields
        :return: response whether request is successful
        """

        title: str = request.query_params.get("title", "")
        if not title:
            return Response(
                data="Title must not be empty.",
                status=HTTP_400_BAD_REQUEST,
            )

        category: str = request.data.get("category", "")

        code = Product.create(
            title=title,
            category=category,
        )

        return Response(
            data={
                "code": code,
            },
            status=HTTP_200_OK,
        )

    def delete(
        self,
        request: Request,
    ) -> Response:
        """
        Delete product by its code.
        :param request: request with "code" field
        :return: response whether request is successful
        """

        code_from_query: str = request.query_params.get("code")
        try:
            code: uuid.UUID = uuid.UUID(code_from_query)
            Product.delete_by_code(code)
        except (TypeError, ValueError, Product.DoesNotExist):
            return Response(
                data="No product with such code.",
                status=HTTP_404_NOT_FOUND,
            )

        return Response(
            data="Product was deleted successfully.",
            status=HTTP_200_OK,
        )


@api_view(["GET"])
def products(
    request: Request,
) -> Response:
    """
    Show multiple products. Pagination included.
    :param request: request with optional "page" and "page_size" fields
    :return: response with page of products
    """

    page_size = 5
    page = 1

    if "page_size" in request.query_params:
        try:
            page_size: int = int(request.query_params.get("page_size"))
            if page_size <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return Response(
                data="Incorrect page size.",
                status=HTTP_400_BAD_REQUEST,
            )

    if "page" in request.query_params:
        try:
            page: int = int(request.query_params.get("page"))
            if page <= 0 or page > Product.objects.count() / page_size:
                raise ValueError
        except (ValueError, TypeError):
            return Response(
                data="Incorrect page.",
                status=HTTP_400_BAD_REQUEST,
            )

    return Response(
        data=Product
             .objects
             .order_by("title")
             .values("title", "category", "code")
             [page_size * (page - 1): page_size * page],
        status=HTTP_200_OK,
    )

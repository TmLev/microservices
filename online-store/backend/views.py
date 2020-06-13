# coding=utf-8

import grpc
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

from api.proto.auth_pb2_grpc import AuthStub
from api.proto.auth_pb2 import (
    Admin,
    Profile,
    Token,
)

from backend.models import Product
from backend.serializers import ProductSerializer


INVALID_CREDENTIALS = Response(
    data={
        "message": "Invalid credentials."
    },
    status=HTTP_401_UNAUTHORIZED,
)
PRODUCT_NOT_FOUND = Response(
    data={
        "message": "No product with such id.",
    },
    status=HTTP_404_NOT_FOUND,
)


def get_profile_by_token(
    request: Request,
) -> Profile:
    """
    Get profile associated with token from request.
    :param request: request with token in header.
    :return: profile (from gRPC specification).
    """

    token_from_request = request.META.get("HTTP_AUTHORIZATION", "").split("Bearer ")[-1]

    auth_grpc = os.environ.get("AUTH_GRPC_HOST") + ":" + os.environ.get("AUTH_GRPC_PORT")

    with grpc.insecure_channel(auth_grpc) as channel:
        stub = AuthStub(channel)
        token = Token(token=token_from_request)
        profile = stub.Verify(token)

    return profile


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

        profile: Profile = get_profile_by_token(request)

        if not profile.has_valid_token:
            return INVALID_CREDENTIALS

        id_: str = request.query_params.get("id")
        try:
            product: Product = Product.get_by_id(id_)
        except (ValueError, TypeError, Product.DoesNotExist):
            return PRODUCT_NOT_FOUND

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

        profile: Profile = get_profile_by_token(request)

        if not profile.has_valid_token or profile.role != Admin:
            return INVALID_CREDENTIALS

        id_: str = request.data.get("id")
        try:
            product: Product = Product.get_by_id(id_)
        except (ValueError, TypeError, Product.DoesNotExist):
            return PRODUCT_NOT_FOUND

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

        profile: Profile = get_profile_by_token(request)

        if not profile.has_valid_token or profile.role != Admin:
            return INVALID_CREDENTIALS

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

        profile: Profile = get_profile_by_token(request)

        if not profile.has_valid_token or profile.role != Admin:
            return INVALID_CREDENTIALS

        id_: str = request.data.get("id")
        try:
            Product.delete_by_id(id_)
        except (TypeError, ValueError, Product.DoesNotExist):
            return PRODUCT_NOT_FOUND

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

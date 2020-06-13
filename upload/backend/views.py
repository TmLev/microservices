# coding=utf-8

import os
import grpc

from django.core.files.uploadedfile import File

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
)
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from api.proto.auth_pb2_grpc import AuthStub
from api.proto.auth_pb2 import (
    Profile,
    Token,
)

from backend.files import save_to_tempdir
from backend.tasks import async_import


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


class ProductUpload(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(
        self,
        request: Request,
        *args,
        **kwargs
    ) -> Response:
        """
        Upload file with products in `.csv` or `.xml` format.
        :param request: request with token in header and file in data.
        :return: response whether request is successful.
        """

        profile: Profile = get_profile_by_token(request)

        if not profile.has_valid_token:
            return Response(
                data={
                    "message": "Invalid credentials."
                },
                status=HTTP_401_UNAUTHORIZED,
            )

        if "file" not in request.data:
            return Response(
                data={
                    "message": "No file uploaded.",
                },
                status=HTTP_400_BAD_REQUEST,
            )

        file: File = request.data["file"]
        format_: str = file.name.split(".")[-1]

        if format_ not in ["csv", "xml"]:
            return Response(
                data={
                    "message": "Invalid format.",
                },
                status=HTTP_400_BAD_REQUEST,
            )

        path, already_exists = save_to_tempdir(file)
        file.close()

        if already_exists:
            return Response(
                data={
                    "message": "File already exists.",
                },
                status=HTTP_400_BAD_REQUEST,
            )

        async_import(path, format_)

        return Response(
            data={
                "message": "Successful upload, product import has started.",
            },
            status=HTTP_200_OK,
        )

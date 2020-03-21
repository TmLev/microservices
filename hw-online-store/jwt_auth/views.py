# coding=utf-8


from django.contrib.auth.base_user import BaseUserManager

from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_405_METHOD_NOT_ALLOWED,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenVerifyView,
)

from jwt_auth.models import Profile


@api_view(["PUT"])
@permission_classes((AllowAny,))
def register_user(
    request: Request,
) -> Response:
    """
    Register new user.
    :param request: contains e-mail and password.
    :return: response whether request is successful.
    """

    email: str = request.data.get("email")
    email = BaseUserManager.normalize_email(email).lower()
    password: str = request.data.get("password")

    if not email or not password:
        return Response(
            data={
                "message": "No email or password provided"
            },
            status=HTTP_400_BAD_REQUEST,
        )

    if Profile.exists(email):
        return Response(
            data={
                "message": "User with such email already exists."
            },
            status=HTTP_400_BAD_REQUEST,
        )

    Profile.register(
        email=email,
        password=password,
    )

    return Response(
        data={
            "message": "User created successfully",
        },
        status=HTTP_200_OK,
    )


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Reroute username to email.
    """

    def post(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
        request.data["username"] = request.data.get("email")
        return super().post(request)


class CustomTokenVerifyView(TokenVerifyView):
    """
    Modify POST method.
    """

    def get(
        self,
        request: Request,
        *args,
        **kwargs
    ) -> Response:
        response = super().post(request)
        if response.status_code == HTTP_200_OK:
            response.data["message"] = "Token is valid."
        return response

    def post(
        self,
        *args,
        **kwargs,
    ):
        return Response(
            data={
                "detail": "Method \"POST\" not allowed.",
            },
            status=HTTP_405_METHOD_NOT_ALLOWED,
        )

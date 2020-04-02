# coding=utf-8


from django.contrib.auth.base_user import BaseUserManager

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import (
    InvalidToken,
    TokenError,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenVerifyView,
    TokenRefreshView,
)

from backend.models import Profile
from backend.utils import (
    message_queue_provider,
    get_according_notification_queue,
    make_confirmation_message,
)


@api_view(["PUT"])
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
    phone_number: str = request.data.get("phone_number", "")
    password: str = request.data.get("password")

    if not email or not password:
        return Response(
            data={
                "message": "No email or password provided."
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

    user = Profile.register(
        email=email,
        password=password,
    )

    queue = get_according_notification_queue(
        prefix="sms" if phone_number else "email",
    )

    body = make_confirmation_message(
        view=confirm_registration,
        confirmation_token=RefreshToken.for_user(user),
    )

    message_queue_provider.send_confirmation(
        queue=queue,
        recipient=phone_number if phone_number else email,
        subject="Registration confirmation",
        body=body,
    )

    device = "phone" if phone_number else "email address"

    return Response(
        data={
            "message": f"User created successfully, "
                       f"check your {device} for confirmation link.",
        },
        status=HTTP_200_OK,
    )


@api_view(["GET"])
def confirm_registration(
    request: Request,
) -> Response:
    """
    Confirm user registration using sent token.
    :param request: contains confirmation token in query params.
    :return: response whether request is successful.
    """

    token = request.query_params.get("token")

    try:
        payload = RefreshToken(
            token=token,
        ).payload
    except TokenError:
        return Response(
            data={
                "message": "Token is invalid or expired.",
            },
            status=HTTP_400_BAD_REQUEST,
        )

    id_ = int(payload["id"])

    Profile.mark_active(
        id_=id_,
    )

    return Response(
        data={
            "message": "Email is verified, registration completed."
        },
        status=HTTP_200_OK,
    )


class CustomTokenRefreshView(TokenRefreshView):
    """
    Change message.
    """

    def post(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
        """
        Do as in docs.
        """

        try:
            response = super().post(request, *args, **kwargs)
        except InvalidToken:
            return Response(
                data={
                    "message": "Token is invalid or expired.",
                },
                status=HTTP_400_BAD_REQUEST,
            )

        return response


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
        """
        Do as in docs.
        """

        request.data["username"] = request.data.get("email")

        return super().post(request)


class CustomTokenVerifyView(TokenVerifyView):
    """
    Verify token.
    """

    def post(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
        """
        Reroute request to TokenVerifyView.
        """

        message: str = "Valid token."
        status: int = HTTP_200_OK

        try:
            super().post(request, *args, **kwargs)
        except InvalidToken:
            message = "Invalid token."
            status = HTTP_400_BAD_REQUEST

        return Response(
            data={
                "message": message,
            },
            status=status,
        )

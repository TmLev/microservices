# coding=utf-8

from django.db import models
from django.contrib.auth.models import User

from api.proto.auth_pb2 import (
    User as GRPCUser,
    Admin as GRPCAdmin,
)


class Profile(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
    )
    role = models.IntegerField(
        choices=(
            (GRPCUser, "User"),
            (GRPCAdmin, "Admin"),
        ),
        default=GRPCUser,
    )

    @staticmethod
    def register(
        email: str,
        password: str,
        role: int = GRPCUser,
        is_active: bool = False,
    ) -> User:
        """
        Register new user.
        """

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            is_active=is_active,
        )
        user.save()

        profile = Profile(
            user=user,
            role=role,
        )
        profile.save()

        return user

    @staticmethod
    def exists(
        email: str,
    ) -> bool:
        return Profile.objects.filter(user__email=email).exists()

    @staticmethod
    def mark_active(
        id_: int,
    ) -> None:
        """
        Mark associated User model active.
        :param id_: User model id.
        :return: nothing.
        """

        user = User.objects.get(id=id_)
        user.is_active = True
        user.save()

        return


    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


    def __str__(
        self,
    ) -> str:
        return self.user.username

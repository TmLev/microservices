# coding=utf-8

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
    )

    @staticmethod
    def register(
        email: str,
        password: str,
    ) -> None:
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
        )
        user.save()
        profile = Profile(
            user=user,
        )
        profile.save()
        return

    @staticmethod
    def exists(
        email: str,
    ) -> bool:
        return Profile.objects.filter(user__email=email).exists()


    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


    def __str__(
        self,
    ) -> str:
        return self.user.username

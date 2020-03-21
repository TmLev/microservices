# coding=utf-8

from django.contrib import admin

from jwt_auth.models import Profile


admin.site.register(Profile)

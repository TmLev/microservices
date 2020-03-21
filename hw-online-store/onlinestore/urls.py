# coding=utf-8

"""
onlinestore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from backend.views import (
    ProductView,
    ListProductView,
    populate,
)

from jwt_auth.views import (
    register_user,
    CustomTokenObtainPairView,
    CustomTokenVerifyView,
)


urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/product", ProductView.as_view()),
    path("api/products", ListProductView.as_view()),
    path("api/populate", populate),

    path("api/register_user", register_user),
    path("api/authorize_user", CustomTokenObtainPairView.as_view()),
    path("api/refresh_token", TokenRefreshView.as_view()),
    path("api/verify_token", CustomTokenVerifyView.as_view()),
]

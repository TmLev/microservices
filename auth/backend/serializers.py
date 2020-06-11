# coding=utf-8

from rest_framework import serializers
from django_grpc_framework import proto_serializers

from api.proto import auth_pb2

from backend.models import Profile


class ProfileProtoSerializer(proto_serializers.ModelProtoSerializer):
    has_valid_token = serializers.BooleanField(default=False)


    class Meta:
        model = Profile
        proto_class = auth_pb2.Profile
        fields = ["has_valid_token", "id", "role"]

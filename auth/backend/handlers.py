# coding=utf-8

from api.proto import auth_pb2_grpc

from backend.services import Auth


def grpc_handlers(server):
    auth_pb2_grpc.add_AuthServicer_to_server(Auth.as_servicer(), server)

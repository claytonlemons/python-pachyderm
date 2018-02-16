# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from client.deploy import deploy_pb2 as client_dot_deploy_dot_deploy__pb2


class APIStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.DeployStorageSecret = channel.unary_unary(
        '/deploy.API/DeployStorageSecret',
        request_serializer=client_dot_deploy_dot_deploy__pb2.DeployStorageSecretRequest.SerializeToString,
        response_deserializer=client_dot_deploy_dot_deploy__pb2.DeployStorageSecretResponse.FromString,
        )


class APIServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def DeployStorageSecret(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_APIServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'DeployStorageSecret': grpc.unary_unary_rpc_method_handler(
          servicer.DeployStorageSecret,
          request_deserializer=client_dot_deploy_dot_deploy__pb2.DeployStorageSecretRequest.FromString,
          response_serializer=client_dot_deploy_dot_deploy__pb2.DeployStorageSecretResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'deploy.API', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))

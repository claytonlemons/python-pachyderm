# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from python_pachyderm.proto.identity import identity_pb2 as src_dot_identity_dot_identity__pb2


class APIStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.SetIdentityServerConfig = channel.unary_unary(
        '/identity.API/SetIdentityServerConfig',
        request_serializer=src_dot_identity_dot_identity__pb2.SetIdentityServerConfigRequest.SerializeToString,
        response_deserializer=src_dot_identity_dot_identity__pb2.SetIdentityServerConfigResponse.FromString,
        )
    self.GetIdentityServerConfig = channel.unary_unary(
        '/identity.API/GetIdentityServerConfig',
        request_serializer=src_dot_identity_dot_identity__pb2.GetIdentityServerConfigRequest.SerializeToString,
        response_deserializer=src_dot_identity_dot_identity__pb2.GetIdentityServerConfigResponse.FromString,
        )
    self.CreateIDPConnector = channel.unary_unary(
        '/identity.API/CreateIDPConnector',
        request_serializer=src_dot_identity_dot_identity__pb2.CreateIDPConnectorRequest.SerializeToString,
        response_deserializer=src_dot_identity_dot_identity__pb2.CreateIDPConnectorResponse.FromString,
        )
    self.UpdateIDPConnector = channel.unary_unary(
        '/identity.API/UpdateIDPConnector',
        request_serializer=src_dot_identity_dot_identity__pb2.UpdateIDPConnectorRequest.SerializeToString,
        response_deserializer=src_dot_identity_dot_identity__pb2.UpdateIDPConnectorResponse.FromString,
        )
    self.ListIDPConnectors = channel.unary_unary(
        '/identity.API/ListIDPConnectors',
        request_serializer=src_dot_identity_dot_identity__pb2.ListIDPConnectorsRequest.SerializeToString,
        response_deserializer=src_dot_identity_dot_identity__pb2.ListIDPConnectorsResponse.FromString,
        )
    self.GetIDPConnector = channel.unary_unary(
        '/identity.API/GetIDPConnector',
        request_serializer=src_dot_identity_dot_identity__pb2.GetIDPConnectorRequest.SerializeToString,
        response_deserializer=src_dot_identity_dot_identity__pb2.GetIDPConnectorResponse.FromString,
        )
    self.DeleteIDPConnector = channel.unary_unary(
        '/identity.API/DeleteIDPConnector',
        request_serializer=src_dot_identity_dot_identity__pb2.DeleteIDPConnectorRequest.SerializeToString,
        response_deserializer=src_dot_identity_dot_identity__pb2.DeleteIDPConnectorResponse.FromString,
        )
    self.CreateOIDCClient = channel.unary_unary(
        '/identity.API/CreateOIDCClient',
        request_serializer=src_dot_identity_dot_identity__pb2.CreateOIDCClientRequest.SerializeToString,
        response_deserializer=src_dot_identity_dot_identity__pb2.CreateOIDCClientResponse.FromString,
        )
    self.UpdateOIDCClient = channel.unary_unary(
        '/identity.API/UpdateOIDCClient',
        request_serializer=src_dot_identity_dot_identity__pb2.UpdateOIDCClientRequest.SerializeToString,
        response_deserializer=src_dot_identity_dot_identity__pb2.UpdateOIDCClientResponse.FromString,
        )
    self.GetOIDCClient = channel.unary_unary(
        '/identity.API/GetOIDCClient',
        request_serializer=src_dot_identity_dot_identity__pb2.GetOIDCClientRequest.SerializeToString,
        response_deserializer=src_dot_identity_dot_identity__pb2.GetOIDCClientResponse.FromString,
        )
    self.ListOIDCClients = channel.unary_unary(
        '/identity.API/ListOIDCClients',
        request_serializer=src_dot_identity_dot_identity__pb2.ListOIDCClientsRequest.SerializeToString,
        response_deserializer=src_dot_identity_dot_identity__pb2.ListOIDCClientsResponse.FromString,
        )
    self.DeleteOIDCClient = channel.unary_unary(
        '/identity.API/DeleteOIDCClient',
        request_serializer=src_dot_identity_dot_identity__pb2.DeleteOIDCClientRequest.SerializeToString,
        response_deserializer=src_dot_identity_dot_identity__pb2.DeleteOIDCClientResponse.FromString,
        )
    self.DeleteAll = channel.unary_unary(
        '/identity.API/DeleteAll',
        request_serializer=src_dot_identity_dot_identity__pb2.DeleteAllRequest.SerializeToString,
        response_deserializer=src_dot_identity_dot_identity__pb2.DeleteAllResponse.FromString,
        )


class APIServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def SetIdentityServerConfig(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetIdentityServerConfig(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def CreateIDPConnector(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def UpdateIDPConnector(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ListIDPConnectors(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetIDPConnector(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DeleteIDPConnector(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def CreateOIDCClient(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def UpdateOIDCClient(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetOIDCClient(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ListOIDCClients(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DeleteOIDCClient(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DeleteAll(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_APIServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'SetIdentityServerConfig': grpc.unary_unary_rpc_method_handler(
          servicer.SetIdentityServerConfig,
          request_deserializer=src_dot_identity_dot_identity__pb2.SetIdentityServerConfigRequest.FromString,
          response_serializer=src_dot_identity_dot_identity__pb2.SetIdentityServerConfigResponse.SerializeToString,
      ),
      'GetIdentityServerConfig': grpc.unary_unary_rpc_method_handler(
          servicer.GetIdentityServerConfig,
          request_deserializer=src_dot_identity_dot_identity__pb2.GetIdentityServerConfigRequest.FromString,
          response_serializer=src_dot_identity_dot_identity__pb2.GetIdentityServerConfigResponse.SerializeToString,
      ),
      'CreateIDPConnector': grpc.unary_unary_rpc_method_handler(
          servicer.CreateIDPConnector,
          request_deserializer=src_dot_identity_dot_identity__pb2.CreateIDPConnectorRequest.FromString,
          response_serializer=src_dot_identity_dot_identity__pb2.CreateIDPConnectorResponse.SerializeToString,
      ),
      'UpdateIDPConnector': grpc.unary_unary_rpc_method_handler(
          servicer.UpdateIDPConnector,
          request_deserializer=src_dot_identity_dot_identity__pb2.UpdateIDPConnectorRequest.FromString,
          response_serializer=src_dot_identity_dot_identity__pb2.UpdateIDPConnectorResponse.SerializeToString,
      ),
      'ListIDPConnectors': grpc.unary_unary_rpc_method_handler(
          servicer.ListIDPConnectors,
          request_deserializer=src_dot_identity_dot_identity__pb2.ListIDPConnectorsRequest.FromString,
          response_serializer=src_dot_identity_dot_identity__pb2.ListIDPConnectorsResponse.SerializeToString,
      ),
      'GetIDPConnector': grpc.unary_unary_rpc_method_handler(
          servicer.GetIDPConnector,
          request_deserializer=src_dot_identity_dot_identity__pb2.GetIDPConnectorRequest.FromString,
          response_serializer=src_dot_identity_dot_identity__pb2.GetIDPConnectorResponse.SerializeToString,
      ),
      'DeleteIDPConnector': grpc.unary_unary_rpc_method_handler(
          servicer.DeleteIDPConnector,
          request_deserializer=src_dot_identity_dot_identity__pb2.DeleteIDPConnectorRequest.FromString,
          response_serializer=src_dot_identity_dot_identity__pb2.DeleteIDPConnectorResponse.SerializeToString,
      ),
      'CreateOIDCClient': grpc.unary_unary_rpc_method_handler(
          servicer.CreateOIDCClient,
          request_deserializer=src_dot_identity_dot_identity__pb2.CreateOIDCClientRequest.FromString,
          response_serializer=src_dot_identity_dot_identity__pb2.CreateOIDCClientResponse.SerializeToString,
      ),
      'UpdateOIDCClient': grpc.unary_unary_rpc_method_handler(
          servicer.UpdateOIDCClient,
          request_deserializer=src_dot_identity_dot_identity__pb2.UpdateOIDCClientRequest.FromString,
          response_serializer=src_dot_identity_dot_identity__pb2.UpdateOIDCClientResponse.SerializeToString,
      ),
      'GetOIDCClient': grpc.unary_unary_rpc_method_handler(
          servicer.GetOIDCClient,
          request_deserializer=src_dot_identity_dot_identity__pb2.GetOIDCClientRequest.FromString,
          response_serializer=src_dot_identity_dot_identity__pb2.GetOIDCClientResponse.SerializeToString,
      ),
      'ListOIDCClients': grpc.unary_unary_rpc_method_handler(
          servicer.ListOIDCClients,
          request_deserializer=src_dot_identity_dot_identity__pb2.ListOIDCClientsRequest.FromString,
          response_serializer=src_dot_identity_dot_identity__pb2.ListOIDCClientsResponse.SerializeToString,
      ),
      'DeleteOIDCClient': grpc.unary_unary_rpc_method_handler(
          servicer.DeleteOIDCClient,
          request_deserializer=src_dot_identity_dot_identity__pb2.DeleteOIDCClientRequest.FromString,
          response_serializer=src_dot_identity_dot_identity__pb2.DeleteOIDCClientResponse.SerializeToString,
      ),
      'DeleteAll': grpc.unary_unary_rpc_method_handler(
          servicer.DeleteAll,
          request_deserializer=src_dot_identity_dot_identity__pb2.DeleteAllRequest.FromString,
          response_serializer=src_dot_identity_dot_identity__pb2.DeleteAllResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'identity.API', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))

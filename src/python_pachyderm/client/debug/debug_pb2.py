# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: client/debug/debug.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='client/debug/debug.proto',
  package='debug',
  syntax='proto3',
  serialized_options=_b('Z/github.com/pachyderm/pachyderm/src/client/debug'),
  serialized_pb=_b('\n\x18\x63lient/debug/debug.proto\x12\x05\x64\x65\x62ug\x1a\x1egoogle/protobuf/wrappers.proto\"\x1f\n\x0b\x44umpRequest\x12\x10\n\x08recursed\x18\x01 \x01(\x08\x32\x44\n\x05\x44\x65\x62ug\x12;\n\x04\x44ump\x12\x12.debug.DumpRequest\x1a\x1b.google.protobuf.BytesValue\"\x00\x30\x01\x42\x31Z/github.com/pachyderm/pachyderm/src/client/debugb\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,])




_DUMPREQUEST = _descriptor.Descriptor(
  name='DumpRequest',
  full_name='debug.DumpRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='recursed', full_name='debug.DumpRequest.recursed', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=67,
  serialized_end=98,
)

DESCRIPTOR.message_types_by_name['DumpRequest'] = _DUMPREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DumpRequest = _reflection.GeneratedProtocolMessageType('DumpRequest', (_message.Message,), dict(
  DESCRIPTOR = _DUMPREQUEST,
  __module__ = 'client.debug.debug_pb2'
  # @@protoc_insertion_point(class_scope:debug.DumpRequest)
  ))
_sym_db.RegisterMessage(DumpRequest)


DESCRIPTOR._options = None

_DEBUG = _descriptor.ServiceDescriptor(
  name='Debug',
  full_name='debug.Debug',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=100,
  serialized_end=168,
  methods=[
  _descriptor.MethodDescriptor(
    name='Dump',
    full_name='debug.Debug.Dump',
    index=0,
    containing_service=None,
    input_type=_DUMPREQUEST,
    output_type=google_dot_protobuf_dot_wrappers__pb2._BYTESVALUE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_DEBUG)

DESCRIPTOR.services_by_name['Debug'] = _DEBUG

# @@protoc_insertion_point(module_scope)

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: python_pachyderm/proto/v2/debug/debug.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from python_pachyderm.proto.v2.pps import pps_pb2 as python__pachyderm_dot_proto_dot_v2_dot_pps_dot_pps__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='python_pachyderm/proto/v2/debug/debug.proto',
  package='debug_v2',
  syntax='proto3',
  serialized_options=b'Z+github.com/pachyderm/pachyderm/v2/src/debug',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n+python_pachyderm/proto/v2/debug/debug.proto\x12\x08\x64\x65\x62ug_v2\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\'python_pachyderm/proto/v2/pps/pps.proto\"V\n\x0eProfileRequest\x12\"\n\x07profile\x18\x01 \x01(\x0b\x32\x11.debug_v2.Profile\x12 \n\x06\x66ilter\x18\x02 \x01(\x0b\x32\x10.debug_v2.Filter\"D\n\x07Profile\x12\x0c\n\x04name\x18\x01 \x01(\t\x12+\n\x08\x64uration\x18\x02 \x01(\x0b\x32\x19.google.protobuf.Duration\"m\n\x06\x46ilter\x12\x0f\n\x05pachd\x18\x01 \x01(\x08H\x00\x12$\n\x08pipeline\x18\x02 \x01(\x0b\x32\x10.pps_v2.PipelineH\x00\x12\"\n\x06worker\x18\x03 \x01(\x0b\x32\x10.debug_v2.WorkerH\x00\x42\x08\n\x06\x66ilter\")\n\x06Worker\x12\x0b\n\x03pod\x18\x01 \x01(\t\x12\x12\n\nredirected\x18\x02 \x01(\x08\"1\n\rBinaryRequest\x12 \n\x06\x66ilter\x18\x01 \x01(\x0b\x32\x10.debug_v2.Filter\">\n\x0b\x44umpRequest\x12 \n\x06\x66ilter\x18\x01 \x01(\x0b\x32\x10.debug_v2.Filter\x12\r\n\x05limit\x18\x02 \x01(\x03\x32\xd1\x01\n\x05\x44\x65\x62ug\x12\x44\n\x07Profile\x12\x18.debug_v2.ProfileRequest\x1a\x1b.google.protobuf.BytesValue\"\x00\x30\x01\x12\x42\n\x06\x42inary\x12\x17.debug_v2.BinaryRequest\x1a\x1b.google.protobuf.BytesValue\"\x00\x30\x01\x12>\n\x04\x44ump\x12\x15.debug_v2.DumpRequest\x1a\x1b.google.protobuf.BytesValue\"\x00\x30\x01\x42-Z+github.com/pachyderm/pachyderm/v2/src/debugb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,google_dot_protobuf_dot_duration__pb2.DESCRIPTOR,python__pachyderm_dot_proto_dot_v2_dot_pps_dot_pps__pb2.DESCRIPTOR,])




_PROFILEREQUEST = _descriptor.Descriptor(
  name='ProfileRequest',
  full_name='debug_v2.ProfileRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='profile', full_name='debug_v2.ProfileRequest.profile', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='filter', full_name='debug_v2.ProfileRequest.filter', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=162,
  serialized_end=248,
)


_PROFILE = _descriptor.Descriptor(
  name='Profile',
  full_name='debug_v2.Profile',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='debug_v2.Profile.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='duration', full_name='debug_v2.Profile.duration', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=250,
  serialized_end=318,
)


_FILTER = _descriptor.Descriptor(
  name='Filter',
  full_name='debug_v2.Filter',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='pachd', full_name='debug_v2.Filter.pachd', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pipeline', full_name='debug_v2.Filter.pipeline', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='worker', full_name='debug_v2.Filter.worker', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
    _descriptor.OneofDescriptor(
      name='filter', full_name='debug_v2.Filter.filter',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=320,
  serialized_end=429,
)


_WORKER = _descriptor.Descriptor(
  name='Worker',
  full_name='debug_v2.Worker',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='pod', full_name='debug_v2.Worker.pod', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='redirected', full_name='debug_v2.Worker.redirected', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=431,
  serialized_end=472,
)


_BINARYREQUEST = _descriptor.Descriptor(
  name='BinaryRequest',
  full_name='debug_v2.BinaryRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='filter', full_name='debug_v2.BinaryRequest.filter', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=474,
  serialized_end=523,
)


_DUMPREQUEST = _descriptor.Descriptor(
  name='DumpRequest',
  full_name='debug_v2.DumpRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='filter', full_name='debug_v2.DumpRequest.filter', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='limit', full_name='debug_v2.DumpRequest.limit', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=525,
  serialized_end=587,
)

_PROFILEREQUEST.fields_by_name['profile'].message_type = _PROFILE
_PROFILEREQUEST.fields_by_name['filter'].message_type = _FILTER
_PROFILE.fields_by_name['duration'].message_type = google_dot_protobuf_dot_duration__pb2._DURATION
_FILTER.fields_by_name['pipeline'].message_type = python__pachyderm_dot_proto_dot_v2_dot_pps_dot_pps__pb2._PIPELINE
_FILTER.fields_by_name['worker'].message_type = _WORKER
_FILTER.oneofs_by_name['filter'].fields.append(
  _FILTER.fields_by_name['pachd'])
_FILTER.fields_by_name['pachd'].containing_oneof = _FILTER.oneofs_by_name['filter']
_FILTER.oneofs_by_name['filter'].fields.append(
  _FILTER.fields_by_name['pipeline'])
_FILTER.fields_by_name['pipeline'].containing_oneof = _FILTER.oneofs_by_name['filter']
_FILTER.oneofs_by_name['filter'].fields.append(
  _FILTER.fields_by_name['worker'])
_FILTER.fields_by_name['worker'].containing_oneof = _FILTER.oneofs_by_name['filter']
_BINARYREQUEST.fields_by_name['filter'].message_type = _FILTER
_DUMPREQUEST.fields_by_name['filter'].message_type = _FILTER
DESCRIPTOR.message_types_by_name['ProfileRequest'] = _PROFILEREQUEST
DESCRIPTOR.message_types_by_name['Profile'] = _PROFILE
DESCRIPTOR.message_types_by_name['Filter'] = _FILTER
DESCRIPTOR.message_types_by_name['Worker'] = _WORKER
DESCRIPTOR.message_types_by_name['BinaryRequest'] = _BINARYREQUEST
DESCRIPTOR.message_types_by_name['DumpRequest'] = _DUMPREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ProfileRequest = _reflection.GeneratedProtocolMessageType('ProfileRequest', (_message.Message,), {
  'DESCRIPTOR' : _PROFILEREQUEST,
  '__module__' : 'python_pachyderm.proto.v2.debug.debug_pb2'
  # @@protoc_insertion_point(class_scope:debug_v2.ProfileRequest)
  })
_sym_db.RegisterMessage(ProfileRequest)

Profile = _reflection.GeneratedProtocolMessageType('Profile', (_message.Message,), {
  'DESCRIPTOR' : _PROFILE,
  '__module__' : 'python_pachyderm.proto.v2.debug.debug_pb2'
  # @@protoc_insertion_point(class_scope:debug_v2.Profile)
  })
_sym_db.RegisterMessage(Profile)

Filter = _reflection.GeneratedProtocolMessageType('Filter', (_message.Message,), {
  'DESCRIPTOR' : _FILTER,
  '__module__' : 'python_pachyderm.proto.v2.debug.debug_pb2'
  # @@protoc_insertion_point(class_scope:debug_v2.Filter)
  })
_sym_db.RegisterMessage(Filter)

Worker = _reflection.GeneratedProtocolMessageType('Worker', (_message.Message,), {
  'DESCRIPTOR' : _WORKER,
  '__module__' : 'python_pachyderm.proto.v2.debug.debug_pb2'
  # @@protoc_insertion_point(class_scope:debug_v2.Worker)
  })
_sym_db.RegisterMessage(Worker)

BinaryRequest = _reflection.GeneratedProtocolMessageType('BinaryRequest', (_message.Message,), {
  'DESCRIPTOR' : _BINARYREQUEST,
  '__module__' : 'python_pachyderm.proto.v2.debug.debug_pb2'
  # @@protoc_insertion_point(class_scope:debug_v2.BinaryRequest)
  })
_sym_db.RegisterMessage(BinaryRequest)

DumpRequest = _reflection.GeneratedProtocolMessageType('DumpRequest', (_message.Message,), {
  'DESCRIPTOR' : _DUMPREQUEST,
  '__module__' : 'python_pachyderm.proto.v2.debug.debug_pb2'
  # @@protoc_insertion_point(class_scope:debug_v2.DumpRequest)
  })
_sym_db.RegisterMessage(DumpRequest)


DESCRIPTOR._options = None

_DEBUG = _descriptor.ServiceDescriptor(
  name='Debug',
  full_name='debug_v2.Debug',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=590,
  serialized_end=799,
  methods=[
  _descriptor.MethodDescriptor(
    name='Profile',
    full_name='debug_v2.Debug.Profile',
    index=0,
    containing_service=None,
    input_type=_PROFILEREQUEST,
    output_type=google_dot_protobuf_dot_wrappers__pb2._BYTESVALUE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Binary',
    full_name='debug_v2.Debug.Binary',
    index=1,
    containing_service=None,
    input_type=_BINARYREQUEST,
    output_type=google_dot_protobuf_dot_wrappers__pb2._BYTESVALUE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Dump',
    full_name='debug_v2.Debug.Dump',
    index=2,
    containing_service=None,
    input_type=_DUMPREQUEST,
    output_type=google_dot_protobuf_dot_wrappers__pb2._BYTESVALUE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_DEBUG)

DESCRIPTOR.services_by_name['Debug'] = _DEBUG

# @@protoc_insertion_point(module_scope)
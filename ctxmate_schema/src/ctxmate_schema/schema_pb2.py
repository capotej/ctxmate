# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: schema.proto
# Protobuf Python Version: 5.29.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    3,
    '',
    'schema.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cschema.proto\x12\x0e\x63txmate_schema\"6\n\x0c\x42\x61\x63kendInput\x12\x15\n\rsystem_prompt\x18\x01 \x01(\x0c\x12\x0f\n\x07\x63ontext\x18\x02 \x01(\x0c\"\x1f\n\rBackendOutput\x12\x0e\n\x06output\x18\x01 \x01(\x0c\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'schema_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_BACKENDINPUT']._serialized_start=32
  _globals['_BACKENDINPUT']._serialized_end=86
  _globals['_BACKENDOUTPUT']._serialized_start=88
  _globals['_BACKENDOUTPUT']._serialized_end=119
# @@protoc_insertion_point(module_scope)

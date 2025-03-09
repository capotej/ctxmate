#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "ctxmate @ ${PROJECT_ROOT}"
# ]
# ///
import sys
import ctxmate.schema_pb2

bi = ctxmate.schema_pb2.BackendInput()
bi.ParseFromString(sys.stdin.buffer.read())
bo = ctxmate.schema_pb2.BackendOutput()
bo.output = bi.ctx
print(bo.SerializeToString())
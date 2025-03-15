import sys
from ctxmate_schema import schema_pb2

def main() -> None:
    bi = schema_pb2.BackendInput()
    bi.ParseFromString(sys.stdin.buffer.read())
    bo = schema_pb2.BackendOutput()
    bo.output = bi.ctx
    print(bo.SerializeToString())
protos:
	protoc -I schema/ --python_out=src/ctxmate --pyi_out=src/ctxmate schema/schema.proto
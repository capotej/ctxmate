protos:
	protoc -I schema/ --python_out=ctxmate --pyi_out=ctxmate schema/schema.proto
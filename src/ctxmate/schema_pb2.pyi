from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BackendInput(_message.Message):
    __slots__ = ("ctx", "model_name", "system_prompt")
    CTX_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_PROMPT_FIELD_NUMBER: _ClassVar[int]
    ctx: str
    model_name: str
    system_prompt: str
    def __init__(self, ctx: _Optional[str] = ..., model_name: _Optional[str] = ..., system_prompt: _Optional[str] = ...) -> None: ...

class BackendOutput(_message.Message):
    __slots__ = ("output",)
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    output: str
    def __init__(self, output: _Optional[str] = ...) -> None: ...

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BackendInput(_message.Message):
    __slots__ = ("system_prompt", "context")
    SYSTEM_PROMPT_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    system_prompt: bytes
    context: bytes
    def __init__(self, system_prompt: _Optional[bytes] = ..., context: _Optional[bytes] = ...) -> None: ...

class BackendOutput(_message.Message):
    __slots__ = ("output",)
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    output: bytes
    def __init__(self, output: _Optional[bytes] = ...) -> None: ...

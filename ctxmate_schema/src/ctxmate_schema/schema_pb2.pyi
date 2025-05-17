from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BackendInput(_message.Message):
    __slots__ = ("system_prompt", "context", "temperature", "top_p", "min_p", "top_k", "min_tokens_to_keep", "seed", "image")
    SYSTEM_PROMPT_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    TOP_P_FIELD_NUMBER: _ClassVar[int]
    MIN_P_FIELD_NUMBER: _ClassVar[int]
    TOP_K_FIELD_NUMBER: _ClassVar[int]
    MIN_TOKENS_TO_KEEP_FIELD_NUMBER: _ClassVar[int]
    SEED_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    system_prompt: bytes
    context: bytes
    temperature: float
    top_p: float
    min_p: float
    top_k: float
    min_tokens_to_keep: int
    seed: int
    image: bytes
    def __init__(self, system_prompt: _Optional[bytes] = ..., context: _Optional[bytes] = ..., temperature: _Optional[float] = ..., top_p: _Optional[float] = ..., min_p: _Optional[float] = ..., top_k: _Optional[float] = ..., min_tokens_to_keep: _Optional[int] = ..., seed: _Optional[int] = ..., image: _Optional[bytes] = ...) -> None: ...

class BackendOutput(_message.Message):
    __slots__ = ("output",)
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    output: bytes
    def __init__(self, output: _Optional[bytes] = ...) -> None: ...

# ctxmate

ctxmate is a tool for managing prompts and contexts. think of it like 'make' but LLM backends instead of GCC or clang

## Installation
`uv tool install ctxmate`

### You can also run it via `uvx`
`uvx run ctxmate`

## Configuration
If a `ctxmate.toml` is found in the root of a directory, `ctxmate` will use that for configuration.


## Backends
These are executables that communicate to LLMs (either locally or via API). They are expected to receive a serialized `BackendInput` payload and output a serialized `BackendOutput`.

## Commands

### `prompts`

Shows all prompts found under prompts/

### `run PROMPT` 

Run a prompt named PROMPT






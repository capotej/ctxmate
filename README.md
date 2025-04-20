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

# Local Development

## Visual Studio Code

1. Make sure to open the ctxmate.code-workspace file

## CLI

_Note: These commands are all run from the `ctxmate/ctxmate_cli` directory unless otherwise specified_

1. Create and activate a virtual environment with `uv`

        $ uv venv
        $ source .venv/bin/activate

2. Install the `ctxmate_cli` package as an editable install

        $ uv pip install -e .

3. Run `ctxmate` (this will work in any directory as long as you are still in the virtual environment)

        $ uv run ctxmate

4. Tests

        $ uv run pytest

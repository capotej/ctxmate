from dataclasses import dataclass
from ctxmate_cli.loading.manager import Manager

def add_prompts_to_manager(manager: Manager, prompt_dir: str) -> None:
    if ":" not in prompt_dir:
        raise Exception(
            "malformed input: '{}', needs to be '<namespace>:<path>'".format(prompt_dir)
        )
    parts = prompt_dir.split(":", 1)
    manager.add_prompt_dir(parts[0], parts[1])

def default_config():
    return Config(
        prompts_dir=("project:prompts",),
        extra_prompts_dir=(),
        backend="ctxmate-echo-backend",
    )

@dataclass(kw_only=True)
class Config:
    """
    Handles reading from CLI arguments or ctxmate.toml found in root directory
    Format:
    ```toml
    [global]
    prompts_directory = "project:prompts"
    backend = "ctxmate-echo-backend"
    ```
    """
    prompts_dir: tuple[str, ...]
    extra_prompts_dir: tuple[str, ...]
    backend: str
        
    def manager(self) -> Manager:
        m: Manager = Manager()
        [ add_prompts_to_manager(m, x) for x in self.prompts_dir]
        [ add_prompts_to_manager(m, x) for x in self.extra_prompts_dir]
        return m

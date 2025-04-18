from ctxmate_cli.loading.manager import Manager

def add_prompts_to_manager(manager: Manager, prompt_dir: str) -> None:
    if ":" not in prompt_dir:
        raise Exception(
            "malformed input: '{}', needs to be '<namespace>:<path>'".format(prompt_dir)
        )
    parts = prompt_dir.split(":", 1)
    manager.add_prompt_dir(parts[0], parts[1])


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

    def __init__(
        self,
        prompts_dir: list[str] = ["project:prompts"],
        extra_prompts_dir: list[str] = [],
        backend: str = "ctxmate-echo-backend",
    ):
        self.manager: Manager = Manager()
        [ add_prompts_to_manager(self.manager, x) for x in prompts_dir]
        [ add_prompts_to_manager(self.manager, x) for x in extra_prompts_dir]

        self.backend: str = backend

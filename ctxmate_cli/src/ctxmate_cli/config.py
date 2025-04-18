from ctxmate_cli.loading.manager import Manager


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
        prompts_directory: list[str] = ["project:prompts"],
        backend: str = "ctxmate-echo-backend",
    ):
        self.manager: Manager = Manager()
        for p in prompts_directory:
            if ":" not in p:
                raise Exception("malformed input: '{}', needs to be '<namespace>:<path>'".format(p))
            parts = p.split(":", 1)
            self.manager.add_prompt_dir(parts[0], parts[1])

        self.backend: str = backend

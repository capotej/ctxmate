import toml

class Config:
    """
    Handles reading from CLI arguments or ctxmate.toml found in root directory
    Format:
    ```toml
    [global]
    prompts_directory = "prompts"
    backend = "ctxmate-echo-backend"
    ```
    """
    def __init__(self, prompts_directory = "prompts", backend = "ctxmate-echo-backend"):
        self.prompts_directory = prompts_directory
        self.backend = backend
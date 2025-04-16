from jinja2 import DictLoader, TemplateNotFound
from ctxmate_cli.config import Config


class BuiltinPromptLoader(DictLoader):
    def __init__(self):
        builtins = {
            "summarize.txt": "Summarize the following: \n {{input}}",
            "system.txt": "You are a helpful assistant",
        }
        super().__init__(builtins)

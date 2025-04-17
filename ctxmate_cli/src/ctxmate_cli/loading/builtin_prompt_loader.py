from jinja2 import DictLoader


class BuiltinPromptLoader(DictLoader):
    def __init__(self):
        builtins = {
            "summarize.txt": "Summarize the following: \n {{input}}",
            "system.txt": "You are a helpful assistant",
        }
        super().__init__(builtins)

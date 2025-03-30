from jinja2 import DictLoader, TemplateNotFound
from ctxmate_cli.config import Config

class BuiltinPromptLoader(DictLoader):
    def __init__(self):
        builtins = {
            'summarize': 'Summarize the following:',
            'system': 'You are a helpful assistant'
        }
        super().__init__(builtins)

    def list_templates(self):
        all:list[str] = super().list_templates() 
        filter_system = lambda x : None if x == 'system' else x
        return list(filter(filter_system, all))



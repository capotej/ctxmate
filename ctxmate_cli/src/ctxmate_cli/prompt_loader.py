from jinja2 import BaseLoader, TemplateNotFound
from os.path import join, exists
from ctxmate_cli.config import Config

import os

class PromptLoader(BaseLoader):
    def __init__(self, c: Config):
        self.config = c

    def get_source(self, environment, template):
        path = join(self.config.prompts_directory, template)
        if not exists(path):
            raise TemplateNotFound(template)
        with open(path) as f:
            source = f.read()
        return source, path, lambda: False

    def list_templates(self) -> list[str]:
        files = []

        if os.path.exists(self.config.prompts_directory):
            for file in os.listdir(self.config.prompts_directory):
                if file == 'system.txt' or file == 'project.txt':
                    continue
                files.append(file)

        return files

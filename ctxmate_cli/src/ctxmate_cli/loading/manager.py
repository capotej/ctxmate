"""
Manager handles the total set of prompt loaders
"""

from jinja2 import BaseLoader, FileSystemLoader, PrefixLoader
from ctxmate_cli.loading.builtin_prompt_loader import BuiltinPromptLoader


class Manager:
    def __init__(self):
        self.loaders: dict[str, BaseLoader] = dict()
        self.loaders["builtin"] = BuiltinPromptLoader()

    def add_prompt_dir(self, namespace: str, dir: str) -> None:
        self.loaders[namespace] = FileSystemLoader(dir)

    def loader(self) -> BaseLoader:
        return PrefixLoader(self.loaders)

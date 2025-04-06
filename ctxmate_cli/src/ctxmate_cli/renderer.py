from collections import deque
from typing import Callable
from jinja2 import Environment, PrefixLoader, TemplateNotFound, Template
from jinja2 import nodes
from dataclasses import dataclass

from ctxmate_cli.config import Config
from ctxmate_cli.context import Context
from ctxmate_cli.project_prompt_loader import ProjectPromptLoader
from ctxmate_cli.builtin_prompt_loader import BuiltinPromptLoader

import io
import os


def find_description(ast: nodes.Template):
    for n in ast.find_all(nodes.Assign):
        name = n.find(nodes.Name)
        if name == None:
            continue
        if name.name == "description":
            value = n.find(nodes.Const)
            if value == None:
                continue
            return value.value

    return ""


@dataclass
class Rendered:
    system_prompt: bytes
    final_prompt: bytes


class Renderer:
    def __init__(self, cfg: Config):
        self.loader = PrefixLoader(
            {"builtin": BuiltinPromptLoader(), "project": ProjectPromptLoader(cfg)}
        )
        self.env = Environment(loader=self.loader, autoescape=False)
        self.prompts: deque[Template] = deque()
        self.system_prompts: deque[Template] = deque()

    def get_loader(self):
        return self.loader

    # TODO Handle .txt or not for name
    def render(self, allowed_files: list[str], *args) -> Rendered:
        # TODO support --no-system
        self._add_default_system_prompt()
        # TODO support --no-project
        self._add_project_prompt()
        
        ctx = Context()
        
        for sp in self.system_prompts:
            ctx.add_system_prompt(sp.render(*args)) 

        for p in self.prompts:
            ctx.add_prompt(p.render(*args)) 

        ctx.write_files(allowed_files)

        ctx.flush()
        return Rendered(
            system_prompt=ctx.final_system_prompt, 
            final_prompt=ctx.final_prompt
        )

    
    def add_prompt(self, name: str) -> None:
        self.prompts.append(self.env.get_template(name))

   
    def _add_default_system_prompt(self) -> None:
        try:
            self.system_prompts.appendleft(self.env.get_template("project/system.txt"))
        except TemplateNotFound:
            self.system_prompts.appendleft(self.env.get_template("builtin/system.txt"))

  
    def _add_project_prompt(self) -> None:
        try:
            self.prompts.appendleft(self.env.get_template("project/project.txt"))
        except TemplateNotFound:
            pass

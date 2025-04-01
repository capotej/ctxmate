from typing import Callable
from jinja2 import Environment, PrefixLoader, TemplateNotFound, Template
from jinja2 import nodes
from dataclasses import dataclass

from ctxmate_cli.config import Config
from ctxmate_cli.project_prompt_loader import ProjectPromptLoader
from ctxmate_cli.builtin_prompt_loader import BuiltinPromptLoader

import io


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
    system_prompt: str
    final_prompt: bytes


class Renderer:
    """Renderers are backed by a BytesIO and are "disposable. Re-use Renderers at your own risk!"""
    def __init__(self, cfg: Config):
        self.loader = PrefixLoader(
            {"builtin": BuiltinPromptLoader(), "project": ProjectPromptLoader(cfg)}
        )
        self.env = Environment(loader=self.loader, autoescape=False)
        # NOTE future proofing for multi-prompt
        self.prompts: list[Template] = []
        self.system_prompt: Template | None = None
        self.files: bytes = bytes()

    def get_loader(self):
        return self.loader
    
    # TODO Handle .txt or not for name
    # TODO Extract to `Renderable` "trait: Callable[...] -> bytes"
    def render(self, *args) -> Rendered:
        # TODO support --no-system
        self._write_system_prompt
        # TODO support --no-project
        self._add_project_prompt
        
        # TODO use a map comprehension instead
        render: Callable[[Template], str] = lambda x: x.render(*args)
        rendered_ctxs: list[str] = list(map(render, self.prompts))

        system_prompt = self.system_prompt.render(*args) if self.system_prompt != None else ""

        with io.BytesIO() as buffer:
            buffer.write("\n".join(rendered_ctxs).encode("utf-8"))
            buffer.write(self.files)
            final_prompt = buffer.getvalue()
            return Rendered(system_prompt=system_prompt, final_prompt=final_prompt)
    
    def write_files(self, allowed_files: list[str]) -> None:
        with io.BytesIO() as buffer:
            for f in allowed_files:
                # txtar format https://pkg.go.dev/golang.org/x/tools/txtar
                buffer.write("-- {} --\n".format(f).encode("utf-8"))
                with open(f, "rb") as file:
                    buffer.write(file.read())
            self.files = buffer.getvalue()
    
    def add_prompt(self, name: str, *args) -> None:
        self.prompts.append(self.env.get_template(name))

    def _write_system_prompt(self) -> None:
        try:
            self.system_prompt = self.env.get_template("project/system.txt")
        except TemplateNotFound:
            self.system_prompt = self.env.get_template("builtin/system.txt")
    
    def _add_project_prompt(self) -> None:
        try:
            self.prompts.append(self.env.get_template("project/project.txt"))
        except TemplateNotFound:
            pass


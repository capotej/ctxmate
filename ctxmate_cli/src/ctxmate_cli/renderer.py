from typing import Callable
from jinja2 import Environment, PrefixLoader, TemplateNotFound, Template
from dataclasses import dataclass

from ctxmate_cli.config import Config
from ctxmate_cli.project_prompt_loader import ProjectPromptLoader
from ctxmate_cli.builtin_prompt_loader import BuiltinPromptLoader



@dataclass
class Rendered:
    system_prompt: str
    final_prompt: str


class Renderer:
    def __init__(self, cfg: Config):
        self.env = Environment(
            loader=PrefixLoader({
                'project': ProjectPromptLoader(cfg),
                'builtin': BuiltinPromptLoader()
            }),
            autoescape=False)

    def render(self, name: str, *args) -> Rendered:
        try:
            system_prompt = self.env.get_template("project/system.txt")
        except TemplateNotFound:
            system_prompt = self.env.get_template("builtin/system.txt")

        ctxs: list[Template] = []

        try:
            project_tmpl: Template = self.env.get_template("project/project.txt")
            ctxs.append(project_tmpl)
        except TemplateNotFound:
            pass
        
        prompt_tmpl = self.env.get_template(name)
        ctxs.append(prompt_tmpl)

        render: Callable[[Template], str] = lambda x : x.render(*args)
        rendered_ctxs: list[str] = list(map(render, ctxs))

        final_prompt = "\n".join(rendered_ctxs)
        rendered = Rendered(system_prompt.render(*args), final_prompt)
        return rendered

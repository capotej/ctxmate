from jinja2 import Environment, FileSystemLoader, select_autoescape
from dataclasses import dataclass

from ctxmate_cli.config import Config

@dataclass
class Rendered:
    system_prompt: str
    final_prompt: str


class Renderer:
    def __init__(self, cfg:Config):
        self.env = Environment(
            loader=FileSystemLoader(cfg.prompts_directory),
            autoescape=False
        )
        self.config = cfg

    def render(self, name:str) -> Rendered:
        system_prompt = self.env.get_template("system.txt")
        project_tmpl = self.env.get_template("project.txt")
        prompt_tmpl = self.env.get_template(name)
        final_prompt = "\n".join([project_tmpl.render(), prompt_tmpl.render()])
        rendered = Rendered(system_prompt.render(), final_prompt)
        return rendered
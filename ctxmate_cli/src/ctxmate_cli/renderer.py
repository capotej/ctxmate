from jinja2 import Environment
from dataclasses import dataclass

from ctxmate_cli.config import Config
from ctxmate_cli.prompt_loader import PromptLoader

@dataclass
class Rendered:
    system_prompt: str
    final_prompt: str

class Renderer:
    def __init__(self, cfg:Config):
        self.env = Environment(
            loader=PromptLoader(cfg),
            autoescape=False
        )

    def render(self, name:str, *args) -> Rendered:
        system_prompt = self.env.get_template("system.txt")
        project_tmpl = self.env.get_template("project.txt")
        prompt_tmpl = self.env.get_template(name)
        final_prompt = "\n".join([project_tmpl.render(*args), prompt_tmpl.render(*args)])
        rendered = Rendered(system_prompt.render(*args), final_prompt)
        return rendered
from ctxmate_cli.config import Config
from ctxmate_cli.renderer import Renderer
import pytest
import os

def test_render():
    current_file_path = os.path.abspath(__file__)
    current_file_base = os.path.dirname(current_file_path)
    print(current_file_base)
    cfg = Config(prompts_directory=current_file_base + "/prompts")
    rdr = Renderer(cfg)
    rndr = rdr.render("001-generate-readme.txt")
    with open(current_file_base + "/prompts/project.txt", "r") as f:
        project = f.read()

    with open(current_file_base + "/prompts/001-generate-readme.txt", "r") as f:
        readme = f.read()

    combined = "\n".join([project,readme])
    assert combined == rndr.final_prompt
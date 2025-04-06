from ctxmate_cli.config import Config
from ctxmate_cli.renderer import Renderer
import pytest
import os


def test_render():
    current_file_path = os.path.abspath(__file__)
    current_file_base = os.path.dirname(current_file_path)
    cfg = Config(prompts_directory=current_file_base + "/prompts")
    rdr = Renderer(cfg)
    rdr.add_prompt("project/001-generate-readme.txt")

    with open(current_file_base + "/prompts/project.txt", "r") as f:
        project = f.read()

    with open(current_file_base + "/prompts/001-generate-readme.txt", "r") as f:
        readme = f.read()

    with open(current_file_base + "/prompts/system.txt", "r") as f:
        systemp = f.read()

    rndr = rdr.render(allowed_files=[])
    combined = "\n".join([project, readme]).encode("utf-8")

    combined = project + "\n" + readme + "\n"

    assert combined.encode("utf-8") == rndr.final_prompt
    assert systemp + "\n" == rndr.system_prompt

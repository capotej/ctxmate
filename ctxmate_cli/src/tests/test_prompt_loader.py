from ctxmate_cli.config import Config
from ctxmate_cli.project_prompt_loader import ProjectPromptLoader
from ctxmate_cli.builtin_prompt_loader import BuiltinPromptLoader
import os


def test_project_prompts():
    current_file_path = os.path.abspath(__file__)
    current_file_base = os.path.dirname(current_file_path)
    cfg = Config(prompts_directory=current_file_base + "/prompts")
    p = ProjectPromptLoader(cfg)
    list_templates = p.list_templates()
    list_templates.sort()
    expected_templates = [
        "project.txt",
        "system.txt",
        "003-test-descriptions.txt",
        "002-test-variables.txt",
        "001-generate-readme.txt",
    ]
    expected_templates.sort()
    assert list_templates == expected_templates


def test_builtin_prompts():
    p = BuiltinPromptLoader()
    list_templates = p.list_templates()
    list_templates.sort()
    expected_templates = ["summarize.txt", "system.txt"]
    expected_templates.sort()
    assert list_templates == expected_templates

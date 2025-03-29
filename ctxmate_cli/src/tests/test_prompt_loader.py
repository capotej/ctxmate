from ctxmate_cli.config import Config
from ctxmate_cli.prompt_loader import PromptLoader
import pytest
import os
import sys

def test_prompt_loader():
    current_file_path = os.path.abspath(__file__)
    current_file_base = os.path.dirname(current_file_path)
    cfg = Config(prompts_directory=current_file_base + "/prompts")
    p = PromptLoader(cfg)
    list_templates = p.list_templates()
    list_templates.sort()
    expected_templates = ['002-test-variables.txt', '001-generate-readme.txt']
    expected_templates.sort()
    assert list_templates == expected_templates
   
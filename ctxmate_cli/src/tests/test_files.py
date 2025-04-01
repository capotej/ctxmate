import os

from ctxmate_cli.files import Files


def test_basic_files():
    current_file_path = os.path.abspath(__file__)
    current_file_base = os.path.dirname(current_file_path)
    args: tuple[str, ...] = (current_file_base + "/test_f*.py",)
    d = Files(args)
    assert "test_files.py" in d.allowed_files()[0]

from ctxmate_cli.hydrator import Hydrator
import os

def test_basic_definer():
    args: tuple[str, ...] = ("hi=there",)
    d = Hydrator(args)
    assert d.dict()["hi"] == "there"
    
def test_multiple():
    args: tuple[str, ...] = ("hi=there","foo=bar")
    d = Hydrator(args)
    assert d.dict()["hi"] == "there"
    assert d.dict()["foo"] == "bar"

def test_arg_splitting():
    args: tuple[str, ...] = ("hi=there","foo=bar==there=go=")
    d = Hydrator(args)
    assert d.dict()["hi"] == "there"
    assert d.dict()["foo"] == "bar==there=go="

def test_url_file_args():
    current_file_path = os.path.abspath(__file__)
    current_file_base = os.path.dirname(current_file_path)
    
    args: tuple[str, ...] = ("myfile=file://" + current_file_base + "/prompts/project.txt",)
    d = Hydrator(args)
    assert d.dict()["myfile"] == "This is text describing the project, which is added to all contexts."

def test_url_http_args():
    current_file_path = os.path.abspath(__file__)
    current_file_base = os.path.dirname(current_file_path)
    
    args: tuple[str, ...] = ("mysite=http://example.com",)
    d = Hydrator(args)
    assert "Example Domain" in d.dict()["mysite"]
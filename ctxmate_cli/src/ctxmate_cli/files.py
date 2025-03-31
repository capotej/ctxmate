"""Handles appending files to the context, respecting .gitignore"""
import os
import io
import glob
from typing import Callable
from gitignore_parser import parse_gitignore

def allowed(f: str) -> bool:
    matchers: list[Callable[...,bool]] = []
    # TODO add a config based denylist
    if os.path.exists(".gitignore"):
        gitmatcher = parse_gitignore(".gitignore")
        matchers.append(gitmatcher)
    for matcher in matchers:
        if matcher(f):
            return False
    return True


class Files:
    def __init__(self, files: tuple[str,...]):
        self.files = list(files)


    def allowed_files(self) -> list[str]:
        all_files = []
        for f in self.files:
            for name in glob.glob(f, recursive=True):
                all_files.append(name)

        return [f for f in all_files if allowed(f)]

    def render_files(self) -> bytes:
        buffer = io.BytesIO()
        for f in self.allowed_files():
            buffer.write("-- {} --\n".format(f).encode("utf-8"))
            with open(f, "rb") as file:
                buffer.write(file.read())
        result = buffer.getvalue()
        buffer.close()
        return result

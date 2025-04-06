import io
import os

class Context:
    """Context is a manager abstracts the concatenation of streams into the final context"""
    def __init__(self):
        self.system_prompt_buffer = io.BytesIO()
        self.prompt_buffer = io.BytesIO()
        self.file_buffer = io.BytesIO()
        self.final_system_prompt: bytes = bytes()
        self.final_prompt: bytes = bytes()
        self.final_files: bytes = bytes()

    def add_system_prompt(self, str: str) -> None:
        self.system_prompt_buffer.write(str.encode("utf-8"))
        self.system_prompt_buffer.write(b"\n")
    
    def add_prompt(self, str: str) -> None:
        self.prompt_buffer.write(str.encode("utf-8"))
        self.prompt_buffer.write(b"\n")
    
    def write_files(self, allowed_files: list[str]) -> None:
        """allowed_files is a list[str] of file paths that are known to exist and are allowed to be seen"""
        for f in allowed_files:
            if os.path.isdir(f):
                continue
            # txtar format https://pkg.go.dev/golang.org/x/tools/txtar
            self.file_buffer.write("-- {} --\n".format(f).encode("utf-8"))
            with open(f, "rb") as file:
                self.file_buffer.write(file.read())

    def flush(self) -> None:
        """writes all the buffers out"""
        self.final_system_prompt = self.system_prompt_buffer.getvalue()
        self.system_prompt_buffer.close()
        self.final_prompt = self.prompt_buffer.getvalue() + self.file_buffer.getvalue()
        self.prompt_buffer.close()
        self.file_buffer.close()
        
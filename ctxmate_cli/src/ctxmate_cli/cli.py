import click
import io
import subprocess
from ctxmate_schema import schema_pb2
import sys
from rich import console
from rich.console import Console
from rich.columns import Columns
from ctxmate_cli.config import Config
from ctxmate_cli.renderer import Renderer
from ctxmate_cli.prompt_loader import PromptLoader


@click.group()
def cli():
    pass


# TODO: --backend
# TODO: --input-files
@click.command()
@click.argument("prompt", nargs=1)
@click.option("--define", "-D", multiple=True)
def run(prompt: str, define):
   """
   ctxmate run prompts/001-prompt.txt -D a_variable=foo -D b_variable=bar
   """
   cfg = Config()
   rdr = Renderer(cfg)
   console = Console()
   console.print("prompt " + prompt)
   console.print("template_vars " + ",".join(define))
    

@click.command()
def prompts():
   """
   ctxmate prompts
   """
   cfg = Config()
   p = PromptLoader(cfg)
   console = Console()
   console.print(Columns(p.list_templates(), title="prompts"))


# TODO: --backend
# TODO: --input-files
@click.command()
@click.argument("input", type=click.File("rb"))
def prompt(input: io.BufferedReader):
   """
   This script works similar to the Unix `cat` command but it writes
   inout - foo.txt
   """

   bi = schema_pb2.BackendInput()
   bi.ctx = input.read()
   i = bi.SerializeToString()
   backend_output: subprocess.CompletedProcess = subprocess.run(
      ["ctxmate-echo-backend"], shell=True, input=i, capture_output=True, check=True
   )
   bo = schema_pb2.BackendOutput()
   bo.output = backend_output.stdout
   bo.ParseFromString(i)
   sys.stdout.write(bo.output.decode("utf-8"))


cli.add_command(run)
cli.add_command(prompts)

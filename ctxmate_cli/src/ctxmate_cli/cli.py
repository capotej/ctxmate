import click
import io
import subprocess
from ctxmate_schema import schema_pb2
import sys

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
@click.argument("template_args", nargs=-1)
def run(prompt:str, template_args:tuple[str,...]):
   """
   ctxmate run prompts/001-prompt.txt a_variable:foo b_variable:bar
   """
   cfg = Config()
   rdr = Renderer(cfg)
   rndrd = rdr.render(prompt, template_args)
   print(rndrd.final_prompt)

@click.command()
def prompts():
   """
   ctxmate prompts
   """
   cfg = Config()
   p = PromptLoader(cfg)
   print(p.list_templates())

# TODO: --backend 
# TODO: --input-files
@click.command()
@click.argument("input", type=click.File("rb"))
def prompt(input:io.BufferedReader):
   """This script works similar to the Unix `cat` command but it writes
      inout - foo.txt
   """

   bi = schema_pb2.BackendInput()
   bi.ctx = input.read()
   i = bi.SerializeToString()
   backend_output:subprocess.CompletedProcess = subprocess.run(["ctxmate-echo-backend"], shell=True, input=i, capture_output=True, check=True)
   bo = schema_pb2.BackendOutput()
   bo.output = backend_output.stdout
   bo.ParseFromString(i)
   sys.stdout.write(bo.output.decode("utf-8"))

cli.add_command(run)
cli.add_command(prompts)

import click
import io
import subprocess
from ctxmate_schema import schema_pb2
import sys
from rich import console
from rich.console import Console
from rich.table import Table
from jinja2 import Environment, meta
from ctxmate_cli.config import Config
from ctxmate_cli.renderer import Renderer, find_description
from ctxmate_cli.project_prompt_loader import ProjectPromptLoader
from ctxmate_cli.builtin_prompt_loader import BuiltinPromptLoader


@click.group()
def cli():
    pass


@click.command()
@click.argument("prompt", nargs=1)
@click.option("--define", "-D", multiple=True)
@click.option(
    "--backend", "-b", show_default=True, default="ctxmate-echo-backend", required=False
)
@click.option(
    "--prompts-dir", "-P", show_default=True, default="prompts", required=False
)
@click.argument("stdin", type=click.File("r"), required=False)
def run(
    prompt: str, define, backend: str, prompts_dir: str, stdin: io.BufferedReader | None
):
    """
    ctxmate run builtin/summarize -D a_variable=foo -D b_variable=bar
    """
    cfg = Config(backend=backend, prompts_directory=prompts_dir)
    rdr = Renderer(cfg)
    console = Console()
    console.print(define)
    if stdin:
        inp = str(stdin.read())
        console.print(rdr.render(prompt, {"input": inp}))
    else:
        console.print(rdr.render(prompt))


@click.command()
@click.option(
    "--prompts-dir", "-P", show_default=True, default="prompts", required=False
)
def prompts(prompts_dir: str):
    """
    ctxmate prompts
    """
    cfg = Config(prompts_directory=prompts_dir)
    pl = ProjectPromptLoader(cfg)
    bl = BuiltinPromptLoader()
    env = Environment()
    table = Table(title="Prompts")
    table.add_column("Name")
    table.add_column("Variables")
    table.add_column("Description")

    # TODO replace with prefixloader?
    # TODO move to renderer
    for t in bl.list_templates():
        tmpl = bl.get_source(env, t)
        ast = env.parse(tmpl[0])
        # print(ast.dump())
        undeclared = meta.find_undeclared_variables(ast)
        description = find_description(ast)
        table.add_row("builtin/" + t, ",".join(list(undeclared)), description)

    for t in pl.list_templates():
        tmpl = pl.get_source(env, t)
        ast = env.parse(tmpl[0])
        undeclared = meta.find_undeclared_variables(ast)
        description = find_description(ast)
        table.add_row("project/" + t, ",".join(list(undeclared)), description)

    console = Console()
    console.print(table)

    # console.print(Columns(p.list_templates(), title="Project Prompts"))


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

import click
import io
import subprocess
from ctxmate_schema import schema_pb2
from rich.console import Console
from rich.table import Table
from jinja2 import Environment, meta
from ctxmate_cli.config import Config
from ctxmate_cli.renderer import Renderer, find_description
from ctxmate_cli.hydrator import Hydrator
from ctxmate_cli.files import Files


@click.group()
def cli():
    pass


@click.command()
# TODO should we take multiple prompts?
@click.argument("prompt", nargs=1)
@click.option("--define", "-D", multiple=True)
@click.option(
    "--backend", "-b", show_default=True, default="ctxmate-echo-backend", required=False
)
@click.option(
    "--prompts-dir", "-P", show_default=True, default="prompts", required=False
)
@click.option("--include", "-I", required=False, multiple=True)
@click.argument("input", type=click.File("r"), required=False)
# TODO --no-project argument to omit the project prompt
# TODO --no-system argument to omit the system prompt
def render(
    prompt: str,
    define,
    backend: str,
    prompts_dir: str,
    include,
    input: io.BufferedReader | None,
):
    """
    ctxmate render builtin/summarize.txt -D a_variable=foo -D b_variable=bar
    """
    cfg = Config(backend=backend, prompts_directory=prompts_dir)
    files = Files(include)
    rdr = Renderer(cfg)
    # console.print(files.render_files())

    h = Hydrator(define)
    vars = h.dict()
    if input:
        inp = str(input.read())
        vars["input"] = inp
    rdr.add_prompt(prompt)
    rendered = rdr.render(files.allowed_files(), vars)

    # TODO extract to executor
    bi = schema_pb2.BackendInput()
    bi.system_prompt = rendered.system_prompt
    bi.context = rendered.final_prompt
    i = bi.SerializeToString()
    backend_output: subprocess.CompletedProcess = subprocess.run(
        ["ctxmate-echo-backend"], shell=True, input=i, capture_output=True, check=True
    )
    bo = schema_pb2.BackendOutput()
    bo.output = backend_output.stdout
    bo.ParseFromString(i)

    console = Console()
    console.print(bo.output)


# TODO show system and project prompts
@click.command()
@click.option(
    "--prompts-dir", "-P", show_default=True, default="prompts", required=False
)
def prompts(prompts_dir: str):
    """
    ctxmate prompts
    """
    cfg = Config(prompts_directory=prompts_dir)
    rdr = Renderer(cfg)
    env = Environment()
    table = Table(title="Available Prompts")
    table.add_column("Name")
    table.add_column("Variables")
    table.add_column("Included By Default")
    table.add_column("Description")

    loader = rdr.loader
    overrides_default_system_prompt: bool = len([x for x in loader.list_templates() if "project/system.txt" in x]) == 0

    for t in loader.list_templates():
        # TODO move to renderer
        tmpl = loader.get_source(env, t)
        ast = env.parse(tmpl[0])
        # print(ast.dump())
        undeclared = meta.find_undeclared_variables(ast)
        description = find_description(ast)
        if overrides_default_system_prompt:
            if "project/system.txt" in t:
                table.add_row(t, ",".join(list(undeclared)), "Yes", description)
        else:
            if "builtin/system.txt" in t:
                table.add_row(t, ",".join(list(undeclared)), "Yes", description)
            
        if "project/project.txt" in t in t:
            table.add_row(t, ",".join(list(undeclared)), "Yes", description)
        else:
            table.add_row(t, ",".join(list(undeclared)), "", description)

    console = Console()
    console.print(table)

    # console.print(Columns(p.list_templates(), title="Project Prompts"))


cli.add_command(render)
cli.add_command(prompts)

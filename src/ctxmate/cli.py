import click
import io
import subprocess
import schema_pb2
import sys

@click.group()
def cli():
   pass
   
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
   backend_output:subprocess.CompletedProcess = subprocess.run(["backends/echo.py"], shell=True, input=i, capture_output=True, check=True)
   bo = schema_pb2.BackendOutput()
   bo.output = backend_output.stdout
   bo.ParseFromString(i)
   sys.stdout.write(bo.output.decode("utf-8"))

@click.command()
def another():
   """This script works similar to the Unix `cat` command but it writes
      inout - foo.txt
   """
   try:
      import venv
   except ImportError:
      print("The 'venv' module is not available.")
      sys.exit(1)

   if hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix:
      print(f"Running in a virtual environment: {sys.prefix}")
   else:
      print("Not running in a virtual environment.")

cli.add_command(another)
cli.add_command(prompt)

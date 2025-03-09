import click
import io
import subprocess
import schema_pb2
import sys

@click.command()
@click.argument("input", type=click.File("rb"))
def cli(input:io.BufferedReader):
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
   sys.stdout.write(bo.output)
   

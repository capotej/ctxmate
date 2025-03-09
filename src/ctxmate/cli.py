import click
import io
import subprocess
import schema_pb2

@click.command()
@click.argument("input", type=click.File("rb"), nargs=-1)
@click.argument("output", type=click.File("wb"))
def cli(input: io.BufferedReader, output:click.File):
   """This script works similar to the Unix `cat` command but it writes
      inout - foo.txt
   """

   bi = schema_pb2.BackendInput()
   bi.ctx = input[0].read()
   i = bi.SerializeToString()
   output:subprocess.CompletedProcess = subprocess.run(["backends/echo.py"], shell=True, input=i, capture_output=True, check=True)
   bo = schema_pb2.BackendOutput()
   bo.output = output.stdout
   bo.ParseFromString(i)
   print(bo.output)
   

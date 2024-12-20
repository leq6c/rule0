import cmd.example
import cmd.server
import getpass
import os

import click


@click.group()
def cli():
    pass

@cli.command()
def example():
    cmd.example.run()

@cli.command()
@click.option("--port", type=int, default=8080)
def server(port: int):
    cmd.server.spawn_server(port)

if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

    cli()